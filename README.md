# 원티드 프리온보딩 백엔드 코스 5차 선발과제

## 요구사항

1. 채용공고를 등록합니다.

   POST /recruits

   - `RecruitDetailSerializer`를 이용하여 채용공고에 필요한 데이터의 validation을 진행
   - view에서 company_id의 존재여부와 해당 company_id가 실제 존재하는 데이터인지 validation 진행
   - 정상적인 데이터면 채용공고를 등록 후 채용공고를 반환

2. 채용공고를 수정합니다.

   PUT /recruits/\<id>

   - id 값을 받아와 기존 채용공고를 검색 -> 없을 경우 NotFound 처리
   - `RecruitDetailSerializer`를 이용하여 partial로 설정 후 data validation 수행
   - company_id는 변경이 불가능하므로 따로 받지 않음
   - 정상적인 데이터면 채용공고를 수정 후 채용공고를 반환

3. 채용공고를 삭제합니다.

   DELETE /recruits/\<id>

   - id 값을 받아와 기존 채용공고를 검색 -> 없을 경우 NotFound 처리
   - 채용공고 삭제 후 status 204 반환

4. 채용공고 목록을 가져옵니다.

   GET /recruits

   - 채용공고를 모두 가져온 후 반환

5. 채용공고 검색 기능 구현

   GET /recruits/?search=\<query>

   - search query parameter를 가져온 후 `position`, `skill`, `company__name`에 대해 filter 수행

6. 채용 상세 페이지를 가져옵니다.

   GET /recruits/\<id>

   - 채용리스트와 상세페이지에 `채용내용`이 서로 달라야해서 Serializer를 리스트와 디테일로 구분
   - Serializer를 구분한 후 viewset으로 구현하면 복잡도가 늘어나는 것 같아 가독성을 위해 API View로 변경하게 됨
   - 다른 회사가 올린 채용공고를 찾기 위해 `values_list`를 이용하여 id 값만 추출

7. 사용자는 채용공고에 지원합니다

   POST /recruits/\<id>/applies

   - 사용자 ID와 채용공고 ID는 URL와 request에 이미 포함되어 있으므로 데이터를 받지 않음
   - Apply Model에 기존 지원내용이 포함되어 있으면 에러 발생
