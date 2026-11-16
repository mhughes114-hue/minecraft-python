from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from mc.net.minecraft.client.render.ThreadDownloadImage import ThreadDownloadImage


class ThreadDownloadImageTests(unittest.TestCase):
    def test_rate_limit_uses_default_skin_without_traceback(self):
        image_data = type("ImageData", (), {"image": None})()
        downloader = ThreadDownloadImage(image_data, "https://example.com/profile", None)
        output = StringIO()
        rate_limit = HTTPError(
            "https://example.com/profile", 429, "Too Many Requests", None, None
        )

        with patch(
            "mc.net.minecraft.client.render.ThreadDownloadImage.urllib.request.urlopen",
            side_effect=rate_limit,
        ), redirect_stdout(output):
            downloader.run()

        self.assertIsNone(image_data.image)
        self.assertIn("HTTP 429", output.getvalue())
        self.assertNotIn("Traceback", output.getvalue())


if __name__ == "__main__":
    unittest.main()
