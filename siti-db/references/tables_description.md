# 시티 DB 테이블 설명

SQL 작성 전 이 문서를 참고해 올바른 테이블을 선택한다.

## public 스키마

### 사용자
| 테이블명 | 설명 |
|---------|------|
| `user` | 사용자 계정 |
| `user_auth_email` | 이메일 인증 정보 |
| `user_auth_social` | 소셜 로그인 정보 (카카오 등) |
| `user_block` | 사용자 차단 목록 |
| `user_delete_reason` | 탈퇴 사유 |
| `user_fcm_token` | 푸시 알림 토큰 |
| `user_follow` | 팔로우 관계 |
| `user_hidden_comments` | 숨긴 댓글 |
| `user_hidden_posts` | 숨긴 게시글 |
| `user_identity_verification_history` | 본인인증 이력 |
| `user_pass_identity` | 패스 본인인증 정보 |
| `user_report` | 사용자 신고 |
| `user_suspension_history` | 계정 정지 이력 |

### 공연/작품
| 테이블명 | 설명 |
|---------|------|
| `production` | 공연 작품 (뮤지컬, 연극 등) |
| `performance` | 공연 회차 (날짜/시간별) |
| `performance_cast` | 공연 회차별 출연진 |
| `performance_user` | 공연 관람 사용자 |
| `cast` | 출연진 (배우) |
| `cast_user` | 출연진-사용자 연결 |
| `theater` | 극장 정보 |
| `venue` | 공연장 (극장 내 홀) |
| `seat` | 좌석 정보 |
| `genre` | 장르 (뮤지컬, 연극, 콘서트 등) |
| `sub_genre` | 세부 장르 |
| `company` | 공연 제작사/기획사 |

### 예매
| 테이블명 | 설명 |
|---------|------|
| `booking_site` | 예매처 (인터파크, 멜론티켓 등) |
| `production_booking_site` | 작품-예매처 연결 |
| `production_booking_site_url` | 작품별 예매 URL |
| `production_seat_price` | 작품별 좌석 등급/가격 |
| `production_edit_request` | 작품 정보 수정 요청 |

### 티켓북
| 테이블명 | 설명 |
|---------|------|
| `ticket` | **티켓 정보 — 티켓 관련 조회는 이 테이블을 사용** |
| `ticket_book` | ⚠️ 현재 미사용 — 조회하지 말 것 |
| `ticket_book_image` | ⚠️ 현재 미사용 |
| `ticket_book_media` | ⚠️ 현재 미사용 |
| `ticket_book_performance_mapping` | ⚠️ 현재 미사용 |
| `ticket_cast` | 티켓별 출연진 |
| `ticket_parsing_log` | 티켓 파싱 로그 |
| `ticket_status_log` | 티켓 상태 변경 로그 |
| `ticket_verification` | 티켓 인증 정보 |

### 커뮤니티
| 테이블명 | 설명 |
|---------|------|
| `review` | 공연 리뷰 |
| `review_media` | 리뷰 첨부 미디어 |
| `post` | 게시글 |
| `post_media` | 게시글 첨부 미디어 |
| `post_reaction` | 게시글 반응 (좋아요 등) |
| `post_report` | 게시글 신고 |
| `post_views` | 게시글 조회수 |
| `comment` | 댓글 |
| `comment_closure` | 댓글 계층 구조 (클로저 테이블) |
| `comment_reaction` | 댓글 반응 |
| `comment_report` | 댓글 신고 |

### 토픽/채널
| 테이블명 | 설명 |
|---------|------|
| `topic` | 토픽 (카테고리) |
| `topic_follow` | 토픽 팔로우 |
| `topic_play` | 토픽-공연 연결 |
| `channel` | 채널 |
| `channel_entity` | 채널 구성 엔티티 |
| `channel_read_state` | 채널 읽음 상태 |

### 미디어/콘텐츠
| 테이블명 | 설명 |
|---------|------|
| `media` | 미디어 파일 (이미지, 영상) |
| `media_tag` | 미디어 태그 |
| `tag` | 태그 |
| `daily_content` | 데일리 콘텐츠 |
| `folders` | 폴더 (북마크 그룹) |
| `folder_production` | 폴더-작품 연결 |

### 알림/공지
| 테이블명 | 설명 |
|---------|------|
| `notification` | 알림 |
| `notifications` | 알림 목록 |
| `notice` | 공지사항 |
| `inquiry` | 문의 |
| `inquiry_media` | 문의 첨부 미디어 |

### 기타
| 테이블명 | 설명 |
|---------|------|
| `interaction` | 상호작용 이력 |
| `search_history` | 검색 기록 |
| `reason` | 사유 코드 (신고/탈퇴 등) |
| `migrations` | DB 마이그레이션 이력 |
| `schema_migrations` | 스키마 마이그레이션 이력 |

---

## kopis 스키마 (공연예술통합전산망)

| 테이블명 | 설명 |
|---------|------|
| `kopis.facility` | 공연 시설 정보 |
| `kopis.facility_list` | 시설 목록 |
| `kopis.performance` | KOPIS 공연 정보 |
| `kopis.performance_list` | KOPIS 공연 목록 |
| `kopis.performance_place` | KOPIS 공연 장소 |
| `kopis.marker` | 지도 마커 |
| `kopis.relate` | 관련 공연 연결 |
| `kopis.transformation_progress` | 데이터 변환 진행 상태 |
| `kopis.kopis_ingest_history` | KOPIS 데이터 수집 이력 |
