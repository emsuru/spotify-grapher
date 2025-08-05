# FEATURE: Spotify Data Upload & Processing

## FEATURE:
Enable users to upload their Spotify data export (zip file) and process it into a normalized format for visualization. Handle both the quick export (1 year, ~20MB) and full lifetime export (all history, ~200MB+).

## EXAMPLES:

### Data Processing (`examples/data_processing.py`)
- `load_spotify_data_from_zip()`: Extracts and concatenates JSON files from Spotify zip
- `get_data_summary()`: Provides overview statistics of the uploaded data
- Handles two export formats:
  - Quick export: Files with "StreamingHistory" prefix
  - Full export: Files with "Streaming_History_Audio_" prefix

### Key Patterns:
```python
# Handle different Spotify export formats
if 'StreamingHistory' in filename:
    # Quick export format
    columns = ['endTime', 'artistName', 'trackName', 'msPlayed']
elif 'Streaming_History_Audio_' in filename:
    # Full export format  
    columns = ['ts', 'master_metadata_album_artist_name', 
               'master_metadata_track_name', 'ms_played']
```

## DOCUMENTATION:

### Spotify Data Export Format
- Quick Export (1 year):
  - Contains: StreamingHistory0.json, StreamingHistory1.json, etc.
  - Fields: endTime, artistName, trackName, msPlayed
  - Size: Usually 10-50MB
  
- Full Export (lifetime):
  - Contains: Streaming_History_Audio_2013-2024_0.json, etc.
  - Fields: ts, master_metadata_*, ms_played, reason_start, reason_end, shuffle, skipped
  - Size: Can be 200MB+
  - Request time: Up to 30 days from Spotify

### API Endpoints Needed:
- `POST /api/uploads` - Initiate upload, return upload_id
- `POST /api/uploads/{upload_id}/file` - Stream file chunks
- `GET /api/uploads/{upload_id}/status` - Check processing status
- `GET /api/uploads/{upload_id}/summary` - Get data summary after processing

## OTHER CONSIDERATIONS:

### Security & Validation:
- **Zip Bomb Protection**: Limit extraction size to 500MB uncompressed
- **File Type Validation**: Only accept .zip files, verify magic bytes
- **JSON Validation**: Ensure files match expected Spotify schema
- **Privacy**: Never log actual song/artist names, only aggregate stats

### Performance Optimization:
- **Chunked Upload**: Use resumable uploads for large files
- **Background Processing**: Use Celery for processing after upload
- **Streaming Parser**: Don't load entire JSON files into memory at once
- **Database Batching**: Insert records in batches of 1000

### Error Cases:
- Corrupted zip file → "Unable to read export file"
- Wrong file type → "Please upload your Spotify data export"
- Missing expected files → "This doesn't appear to be a Spotify export"
- Processing timeout → "Large file processing, check back in a few minutes"

### Gotchas:
- Some users have HUGE exports (500MB+) with 500k+ streams
- Spotify sometimes includes malformed JSON (extra commas)
- The 'msPlayed' field can be 0 for skipped tracks
- Not all tracks have metadata (local files show as null)
- User might upload while another upload is processing