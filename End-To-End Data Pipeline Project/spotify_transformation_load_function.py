import json
import boto3
from datetime import datetime
from io import StringIO
import pandas as pd

def album(data):
    album_list = []
    for row in data['items']:
        album_id =  row['track']['album']['id']
        album_name = row['track']['album']['name']
        album_release_date = row['track']['album']['release_date']
        album_total_tracks = row['track']['album']['total_tracks']
        album_external_urls = row['track']['album']['external_urls']['spotify']
        album_element = {'album_id': album_id, "album_name": album_name, 'album_release_date': album_release_date, "album_total_tracks": album_total_tracks, "album_external_urls": album_external_urls}
        album_list.append(album_element)
    return album_list
    
def artist(data):
    artist_list = []
    for row in data['items']:
        for key, value in row.items():
            if key == 'track':
                for artist in value['artists']:
                    artist_external_url = artist['external_urls']['spotify']
                    artist_name = artist['name']
                    artist_id = artist['id']
                    artist_href = artist['href']
                    artist_element = {'artist_id': artist_id, 'artist_name': artist_name, 'artist_external_url': artist_external_url, 'artist_href': artist_href}
                    artist_list.append(artist_element)
    return artist_list
    
def songs(data):
    song_list = []
    for row in data['items']:
        song_id = row['track']['id']
        song_name = row['track']['name']
        song_duration = row['track']['duration_ms']
        song_url = row['track']['external_urls']['spotify']
        song_popularity = row['track']['popularity']
        song_added = row['added_at']
        album_id = row['track']['album']['id']
        artist_id = row['track']['album']['artists'][0]['id']
        song_element = {'song_id':song_id,'song_name':song_name,'duration_ms':song_duration,'url':song_url,
                        'popularity':song_popularity,'song_added':song_added,'album_id':album_id,
                        'artist_id':artist_id
                       }
        song_list.append(song_element)
    return song_list
    
def lambda_handler(event, context):
    
    s3 = boto3.client('s3')
    Bucket = "spotify-etl-project-dinesh"
    Key = "raw_data/to_processed/"
    
    spotify_data = []
    spotify_keys = []
    for file in s3.list_objects(Bucket =  Bucket, Prefix = Key)['Contents']:
        file_key = file['Key']
        if file_key.split('.')[-1] == 'json':
            response = s3.get_object(Bucket =  Bucket, Key = file_key)
            content = response['Body']
            jsonObject = json.loads(content.read())
            print(jsonObject)
            spotify_data.append(jsonObject)
            spotify_keys.append(file_key)
            
    
    for data in spotify_data:
        album_list = album(data)
        artist_list = artist(data)
        song_list = songs(data)
        
        album_df = pd.DataFrame.from_dict(album_list)
        album_df['album_release_date'] = pd.to_datetime(album_df['album_release_date'])
        album_df = album_df.drop_duplicates(subset = ['album_id'])
        
        artist_df = pd.DataFrame.from_dict(artist_list)
        artist_df = artist_df.drop_duplicates(subset = ['artist_id'])
        
        song_df = pd.DataFrame.from_dict(song_list)
        song_df = song_df.drop_duplicates(subset = ['song_id'])
        song_df['song_added'] =  pd.to_datetime(song_df['song_added'])
        
        songs_key = "transformed_data/songs_data/songs_transformer_" + str(datetime.now()) + ".csv"
        song_buffer = StringIO()
        song_df.to_csv(song_buffer, index = False)
        song_content = song_buffer.getvalue()
        s3.put_object(Bucket = Bucket, Key= songs_key, Body = song_content)
        
        album_key = "transformed_data/album_data/album_transformer_" + str(datetime.now()) + ".csv"
        album_buffer = StringIO()
        album_df.to_csv(album_buffer, index = False)
        album_content = album_buffer.getvalue()
        s3.put_object(Bucket = Bucket, Key= album_key, Body = album_content)
        
        artists_key = "transformed_data/artist_data/artists_transformer_" + str(datetime.now()) + ".csv"
        artists_buffer = StringIO()
        artist_df.to_csv(artists_buffer, index = False)
        artist_content = artists_buffer.getvalue()
        s3.put_object(Bucket = Bucket, Key= artists_key, Body = artist_content)
        
        
    s3_resource = boto3.resource('s3')
    for key in spotify_keys:
        copy_source = {
            'Bucket': Bucket,
            'Key': key
        }
        s3_resource.meta.client.copy(copy_source, Bucket, 'raw_data/processed/' + key.split("/")[-1])    
        s3_resource.Object(Bucket, key).delete()