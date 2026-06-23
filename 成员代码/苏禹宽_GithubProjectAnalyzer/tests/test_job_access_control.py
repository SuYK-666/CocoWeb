from __future__ import annotations

import unittest

from webapp import _create_job, _get_job, create_app


class JobAccessControlTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = create_app().test_client()
        self.job_id = _create_job("https://github.com/example/project", "econ")
        job = _get_job(self.job_id) or {}
        self.token = str(job.get("access_token", ""))

    def test_result_requires_access_token(self) -> None:
        response = self.client.get(f"/api/result/{self.job_id}")

        self.assertEqual(response.status_code, 401)

    def test_result_rejects_invalid_access_token(self) -> None:
        response = self.client.get(f"/api/result/{self.job_id}?token=wrong-token")

        self.assertEqual(response.status_code, 403)

    def test_result_accepts_valid_access_token(self) -> None:
        response = self.client.get(f"/api/result/{self.job_id}?token={self.token}")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["jobId"], self.job_id)
        self.assertEqual(payload["status"], "queued")

    def test_download_requires_access_token_before_status_check(self) -> None:
        response = self.client.get(f"/api/download/{self.job_id}/md")

        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
