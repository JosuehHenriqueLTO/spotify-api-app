import unittest
from unittest.mock import patch, Mock
from src.main import *

class TestSpotifyAPI(unittest.TestCase):

    @patch('src.main.post')
    def test_get_token(self, mock_post):
        mock_response = Mock()
        mock_response.content = json.dumps({"access_token": "mock_token"}).encode('utf-8')
        mock_post.return_value = mock_response

        token = get_token()

        self.assertEqual(token, "mock_token")
        mock_post.assert_called_once()

    def test_get_auth_header(self):
        token = "mock_token"
        expected_header = {
            "Authorization": "Bearer " + token
        }
        self.assertEqual(get_auth_header(token), expected_header)

    @patch('src.main.get')
    def test_search_for_artist(self, mock_get):
        mock_response = Mock()
        mock_response.content = json.dumps({
            "artists": {
                "items": [{"id": "artist_id", "name": "Magyn"}]
            }
        }).encode('utf-8')
        mock_get.return_value = mock_response

        token = "mock_token"
        artist_name = "Magyn"
        result = search_for_artist(token, artist_name)

        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Magyn")
        mock_get.assert_called_once()

    @patch('src.main.get')
    def test_get_songs_by_artists(self, mock_get):
        mock_response = Mock()
        mock_response.content = json.dumps({
            "tracks": [{"name": "Song 1"}, {"name": "Song 2"}]
        }).encode('utf-8')
        mock_get.return_value = mock_response

        token = "mock_token"
        artist_id = "artist_id"
        songs = get_songs_by_artists(token, artist_id)

        self.assertEqual(len(songs), 2)
        self.assertEqual(songs[0]["name"], "Song 1")
        self.assertEqual(songs[1]["name"], "Song 2")
        mock_get.assert_called_once()

if __name__ == '__main__':
    unittest.main()
