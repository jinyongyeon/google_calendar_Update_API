import unittest
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

class GoogleCalendarAPITest(unittest.TestCase):
    def setUp(self):
        SERVICE_ACCOUNT_FILE = 'path service_account.json'
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = build('calendar', 'v3', credentials=credentials)

        # 테스트용 일정 생성
        start_time = datetime.utcnow() + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        event = {
            'summary': '테스트 이벤트',
            'description': '이벤트 설명',
            'location': 'A회의실',
            'start': {'dateTime': start_time.isoformat(), 'timeZone': 'UTC'},
            'end': {'dateTime': end_time.isoformat(), 'timeZone': 'UTC'},
        }
        self.event = self.service.events().insert(calendarId='primary', body=event).execute()

    def tearDown(self):
        # 테스트 이벤트 삭제
        self.service.events().delete(calendarId='primary', eventId=self.event['id']).execute()

    def test_API_001(self):
        try:
            updated_summary = '제목'
            updated_event = self.update_event(summary=updated_summary)
            self.assertEqual(updated_event['summary'], updated_summary)
            print("API_001_summary 값만 있을 경우 응답 확인 결과 : PASS")
        except Exception as e:
            print(f"API_001_summary 값만 있을 경우 응답 확인 결과 : FAIL\n에러메시지 : {e}")

    def test_API_002(self):
        try:
            updated_event = self.update_event(
                summary='제목 업데이트',
                description='설명 업데이트',
                location='B회의실',
                timeZone='Asia/Seoul'
            )
            self.assertEqual(updated_event['summary'], '제목 업데이트')
            self.assertEqual(updated_event['description'], '설명 업데이트')
            self.assertEqual(updated_event['location'], 'B회의실')
            self.assertEqual(updated_event['start']['timeZone'], 'Asia/Seoul')
            self.assertEqual(updated_event['end']['timeZone'], 'Asia/Seoul')
            print("API_002_모든 값이 입력된 경우 응답 확인 결과 : PASS")
        except Exception as e:
            print(f"API_002_모든 값이 입력된 경우 응답 확인 결과 : FAIL\n에러메시지 : {e}")

    def test_API_003(self):
        try:
            updated_event = self.update_event(summary=None)
            self.assertNotIn('summary', updated_event)
            print("API_003_summary 값 만 없는 경우 응답 확인 결과 : PASS")
        except Exception as e:
            print(f"API_003_summary 값 만 없는 경우 응답 확인 결과 : FAIL\n에러메시지 : {e}")

    def test_API_004(self):
        try:
            updated_event = self.update_event(description=None)
            self.assertNotIn('description', updated_event)
            print("API_004_description 값 만 없는 경우 응답 확인 결과 : PASS")
        except Exception as e:
            print(f"API_004_description 값 만 없는 경우 응답 확인 결과 : FAIL\n에러메시지 : {e}")

    def test_API_005(self):
        try:
            updated_event = self.update_event(location=None)
            self.assertNotIn('location', updated_event)
            print("API_005_location 값 만 없는 경우 응답 확인 결과 : PASS")
        except Exception as e:
            print(f"API_005_location 값 만 없는 경우 응답 확인 결과 : FAIL\n에러메시지 : {e}")

    def test_API_006(self):
        try:
            updated_event = self.update_event(timeZone=None)
            self.assertNotIn('timeZone', updated_event)
            print("API_006_timeZone 값 만 없는 경우 응답 확인 결과 : PASS")
        except Exception as e:
            print(f"API_006_timeZone 값 만 없는 경우 응답 확인 결과 : FAIL\n에러메시지 : {e}")

    def test_API_007(self):
        try:
            with self.assertRaises(Exception):
                self.update_event(timeZone='InvalidTimeZone')
            print("API_007_timeZone 잘못된 값이 입력된 경우 응답 확인 결과 : PASS")
        except Exception as e:
            print(f"API_007_timeZone 잘못된 값이 입력된 경우 응답 확인 결과 : FAIL\n에러메시지 : {e}")

    def test_API_008(self):
        try:
            with self.assertRaises(Exception):
                self.update_event(timeZone=12345)
            print("API_008_timeZone 값이string이 아닌 intger로 입력된 경우 응답 확인 결과 : PASS")
        except Exception as e:
            print(f"API_008_timeZone 값이string이 아닌 intger로 입력된 경우 응답 확인 결과 : PASS\n에러메시지 : {e}")

    def update_event(self, summary=None, description=None, location=None, timeZone=None):
        updated_event = {
            'summary': summary,
            'description': description,
            'location': location,
            'start': {'dateTime': self.event['start']['dateTime'], 'timeZone': timeZone or 'UTC'},
            'end': {'dateTime': self.event['end']['dateTime'], 'timeZone': timeZone or 'UTC'},
        }

        return self.service.events().update(
            calendarId='primary', eventId=self.event['id'], body=updated_event).execute()

if __name__ == '__main__':
    unittest.main()