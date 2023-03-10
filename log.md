## 23-03-10
---
- 카테고리 리스트 추출
- 카테고리 별 10페이지까지 책 정보 수집
- ISBN 추출을 위해 상세 페이지 조회


- 상세 페이지 링크가 없는 책이 존재하는 것 같음
- detail = link.select_one('strong h3 a').attrs['href'] 에서 
- NoneType has no attribute 'attrs' 발생
- 정확하게 확인을 하지 못해서 어떤 카테고리에서 에러가 발생했는지 모름
- 마지막 확인 위치 : 매거진..