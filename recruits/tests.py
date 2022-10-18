from rest_framework.test import APITestCase
from recruits.models import Recruit
from companies.models import Company
from users.models import User


def init():
    """초기 데이터베이스 설정"""
    wanted = Company.objects.create(
        name="원티드랩",
        nation="korea",
        area="서울",
    )
    kakao = Company.objects.create(
        name="카카오",
        nation="korea",
        area="서울",
    )
    wanted_recruit = Recruit.objects.create(
        position="Django 백엔드 개발자",
        reward=1000000,
        description="원티드랩에서 백엔드 주니어 개발자를 채용합니다.",
        skill="Python",
        company=wanted,
    )
    kakao_recruit = Recruit.objects.create(
        position="Django 백엔드 개발자",
        reward=500000,
        description="카카오에서 백엔드 주니어 개발자를 채용합니다.",
        skill="Django",
        company=kakao,
    )

    return wanted, kakao, wanted_recruit, kakao_recruit


class TestRecruits(APITestCase):
    def setUp(self):
        self.wanted, self.kakao, self.wanted_recruit, self.kakao_recruit = init()

    def test_all_recruits(self):
        """채용공고 목록 테스트"""
        response = self.client.get("/api/v1/recruits/")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertNotIn("description", data[0])
        self.assertEqual(data[0]["company_name"], self.wanted.name)
        self.assertEqual(data[0]["company_nation"], self.wanted.nation)
        self.assertEqual(data[0]["company_area"], self.wanted.area)
        self.assertEqual(data[0]["position"], self.wanted_recruit.position)
        self.assertEqual(data[0]["reward"], self.wanted_recruit.reward)
        self.assertEqual(data[0]["skill"], self.wanted_recruit.skill)

    def test_search_recruits(self):
        """채용공고 검색 테스트"""
        response = self.client.get("/api/v1/recruits/?search=원티드")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertNotIn("description", data[0])
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["company_name"], self.wanted.name)
        self.assertEqual(data[0]["company_nation"], self.wanted.nation)
        self.assertEqual(data[0]["company_area"], self.wanted.area)
        self.assertEqual(data[0]["position"], self.wanted_recruit.position)
        self.assertEqual(data[0]["reward"], self.wanted_recruit.reward)
        self.assertEqual(data[0]["skill"], self.wanted_recruit.skill)

        response = self.client.get("/api/v1/recruits/?search=Django")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertNotIn("description", data[0])
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["company_name"], self.wanted.name)
        self.assertEqual(data[0]["company_nation"], self.wanted.nation)
        self.assertEqual(data[0]["company_area"], self.wanted.area)
        self.assertEqual(data[0]["position"], self.wanted_recruit.position)
        self.assertEqual(data[0]["reward"], self.wanted_recruit.reward)
        self.assertEqual(data[0]["skill"], self.wanted_recruit.skill)

    def test_create_recruits(self):
        """채용공고 생생 테스트"""
        response = self.client.post("/api/v1/recruits/")
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["detail"], "Company id is required.")

        response = self.client.post("/api/v1/recruits/", {"company_id": 3})
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["detail"], "Company not found.")

        response = self.client.post(
            "/api/v1/recruits/",
            {
                "company_id": self.wanted.id,
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("position", data)
        self.assertIn("reward", data)
        self.assertIn("description", data)
        self.assertIn("skill", data)

        response = self.client.post(
            "/api/v1/recruits/",
            {
                "company_id": self.wanted.id,
                "position": "프론트엔드 주니어 개발자",
                "reward": 300000,
                "description": "프론트엔드 주니어 개발자를 모집합니다.",
                "skill": "React",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["position"], "프론트엔드 주니어 개발자")


class TestRecruit(APITestCase):
    def setUp(self):
        self.wanted, self.kakao, self.wanted_recruit, self.kakao_recruit = init()

    def test_recruit_not_found(self):
        """채용공고 Not Found 테스트"""
        response = self.client.put("/api/v1/recruits/4")
        data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["detail"], "Not found.")

    def test_one_recruit(self):
        """채용공고 상세 테스트"""
        response = self.client.put("/api/v1/recruits/1")
        data = response.json()

        self.assertIn("description", data)
        self.assertEqual(data["skill"], self.wanted_recruit.skill)
        self.assertIsInstance(data, dict)

    def test_update_recruit(self):
        """채용공고 수정 테스트"""
        response = self.client.put("/api/v1/recruits/1", {"company_id": 2})
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(data["company_name"], self.kakao.name)

        response = self.client.put(
            "/api/v1/recruits/1",
            {
                "skill": "Flask",
                "reward": 300000,
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["skill"], "Flask")
        self.assertEqual(data["reward"], 300000)

    def test_delete_recruit(self):
        """채용공고 삭제 테스트"""
        response = self.client.delete("/api/v1/recruits/1")

        self.assertEqual(response.status_code, 204)

        response = self.client.get("/api/v1/recruits/1")

        self.assertEqual(response.status_code, 404)


class TestRecruitApply(APITestCase):
    def setUp(self):
        self.wanted, self.kakao, self.wanted_recruit, self.kakao_recruit = init()
        user = User.objects.create(username="test")
        user.set_password("1234")
        user.save()
        self.user = user

    def test_create_apply(self):
        """채용공고 지원 테스트"""
        response = self.client.post("/api/v1/recruits/1/applies")
        data = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data["detail"], "Authentication credentials were not provided."
        )

        self.client.force_login(self.user)

        response = self.client.post("/api/v1/recruits/1/applies")

        self.assertEqual(response.status_code, 201)

        response = self.client.post("/api/v1/recruits/1/applies")
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["detail"], "동일한 채용공고에 1회만 지원 가능합니다.")
