# FEATURE: Dynamic Visualization Engine

## FEATURE:
Create interactive, shareable visualizations from processed Spotify data. Support both static image generation for sharing and interactive web-based charts for exploration.

## EXAMPLES:

### Visualization Utilities (`examples/visualization.py`)
- `create_horizontal_bar_chart()`: Top tracks/artists bar charts
- `create_time_series_plot()`: Artist listening over time
- `create_listening_pattern_heatmap()`: Hour/day listening patterns
- `create_genre_diversity_plot()`: Pie chart of listening diversity
- Custom formatters for time display (hours, days, etc.)

### Visualization Types:
1. **Top Lists** - Most played tracks, artists, albums
2. **Time Series** - Listening patterns over days/months/years  
3. **Heatmaps** - When you listen (hour of day, day of week)
4. **Comparisons** - Year over year, genre diversity
5. **Discoveries** - First time you heard an artist, longest gaps

## DOCUMENTATION:

### Frontend Charting Libraries:
- **Chart.js** - Simple, responsive charts for basic visualizations
- **D3.js** - Complex, interactive visualizations (heatmaps, network graphs)
- **Recharts** - React-friendly charts if using React frontend

### Visualization API Design:
```typescript
// Request visualization data
GET /api/visualizations/top-artists?
  timeframe=all|year|month&
  limit=10&
  format=json|image

// Response
{
  "data": [...],
  "metadata": {
    "total_items": 1000,
    "timeframe": "2023-01-01 to 2024-01-01"
  },
  "chart_config": {
    "type": "bar",
    "options": {...}
  }
}
```

### Shareable Visualizations:
- Generate unique share URLs: `/share/{visualization_id}`
- Optional privacy: blur artist/song names
- Embed codes for blogs/social media
- Open Graph tags for social previews

## OTHER CONSIDERATIONS:

### Performance:
- **Cache Computed Data**: Store aggregations in database, don't recalculate
- **Progressive Loading**: Load chart, then enhance with interactions
- **Image Generation**: Use matplotlib on backend for static images
- **CDN for Assets**: Serve chart libraries from CDN

### Accessibility:
- **Alt Text**: Generate descriptive alt text for all charts
- **Data Tables**: Provide tabular view option for screen readers
- **High Contrast**: Support high contrast mode
- **Keyboard Navigation**: All interactions keyboard accessible

### Mobile Optimization:
- **Responsive Charts**: Automatically resize and reflow
- **Touch Gestures**: Swipe through time periods, pinch to zoom
- **Simplified Views**: Fewer data points on small screens
- **Native Sharing**: Use Web Share API for mobile sharing

### Common Gotchas:
- **Time Zones**: User's export is in UTC, display in their local time
- **Missing Data**: Handle gaps in listening history gracefully
- **Scale Issues**: Some users have 100x more data than others
- **Color Blindness**: Don't rely only on color to convey information
- **Browser Limits**: Canvas size limits for very large datasets

### Social Features:
- **Comparison Mode**: Overlay friend's data (with permission)
- **Badges/Achievements**: "Night Owl", "Genre Explorer", etc.
- **Playback**: Link to Spotify to play discovered songs
- **Export**: Download visualizations as PNG/SVG/PDF