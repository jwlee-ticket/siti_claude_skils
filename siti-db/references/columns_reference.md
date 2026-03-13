# 시티 DB 컬럼 레퍼런스

쿼리 작성 전 이 문서를 참고해 올바른 컬럼명과 타입을 확인한다.


---

## public 스키마


### public.booking_site

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `name` | text | Y |
| `is_active` | boolean |  |
| `created_at` | timestamp with time zone | Y |
| `renew_name` | text |  |


### public.cast

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `name` | character varying | Y |
| `created_at` | timestamp with time zone | Y |
| `clean_name` | text |  |


### public.cast_user

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `user_id` | bigint | Y |
| `cast_id` | bigint | Y |
| `profile_media_id` | bigint | Y |


### public.channel

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `name` | text | Y |
| `created_at` | timestamp with time zone |  |
| `updated_at` | timestamp with time zone |  |
| `deleted_at` | timestamp with time zone |  |


### public.channel_entity

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `channel_id` | bigint | Y |
| `entity_type` | character varying | Y |
| `entity_id` | bigint | Y |
| `created_at` | timestamp with time zone |  |


### public.channel_read_state

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `user_id` | integer | Y |
| `channel_id` | bigint | Y |
| `last_seen_at` | timestamp with time zone | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |


### public.comment

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `content` | text | Y |
| `user_id` | integer | Y |
| `post_id` | integer | Y |
| `parent_id` | integer |  |
| `like_count` | integer | Y |


### public.comment_closure

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `parent_id` | integer | Y |
| `child_id` | integer | Y |


### public.comment_reaction

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `user_id` | integer | Y |
| `comment_id` | integer | Y |
| `type` | character varying | Y |


### public.comment_report

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `status` | character varying | Y |
| `user_id` | integer | Y |
| `comment_id` | integer | Y |
| `reason_id` | integer | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |


### public.company

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `name` | character varying | Y |
| `logo_url` | character varying |  |
| `business_number` | character varying |  |
| `company_name` | character varying |  |
| `representative_name` | character varying |  |
| `address` | character varying |  |
| `detailed_address` | character varying |  |
| `contact_phone_number` | character varying |  |
| `contact_email` | character varying |  |
| `is_active` | boolean |  |
| `type` | character varying | Y |


### public.daily_content

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `genre` | character varying | Y |
| `content_type` | character varying | Y |
| `production_title` | text | Y |
| `line` | text | Y |


### public.folder_production

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `folder_id` | bigint | Y |
| `production_id` | bigint | Y |
| `order_index` | integer | Y |
| `created_at` | timestamp without time zone | Y |


### public.folders

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `user_id` | integer | Y |
| `name` | character varying | Y |
| `created_at` | timestamp without time zone |  |
| `updated_at` | timestamp without time zone |  |
| `is_group_view_count` | boolean | Y |


### public.genre

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `name` | character varying | Y |


### public.inquiry

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `type` | character varying | Y |
| `content` | text | Y |
| `reply_email` | character varying | Y |


### public.inquiry_media

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `inquiry_id` | integer | Y |
| `type` | character varying | Y |
| `url` | character varying | Y |
| `origin_name` | character varying | Y |


### public.interaction

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `user_id` | bigint | Y |
| `target_id` | bigint | Y |
| `target_type` | character varying | Y |
| `interaction_type` | character varying | Y |
| `metadata` | json |  |
| `created_at` | timestamp with time zone | Y |


### public.media

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `folder_id` | bigint |  |
| `user_id` | bigint |  |
| `url` | text | Y |
| `mime_type` | text |  |
| `target_type` | character varying |  |
| `metadata` | json |  |
| `capacity` | bigint | Y |
| `created_at` | timestamp with time zone | Y |
| `s3_key` | text |  |
| `filename` | character varying |  |
| `target_id` | bigint |  |


### public.media_tag

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `media_id` | bigint | Y |
| `tag_id` | bigint | Y |
| `created_at` | timestamp with time zone | Y |


### public.migrations

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `timestamp` | bigint | Y |
| `name` | character varying | Y |


### public.notice

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `title` | character varying | Y |
| `content` | text | Y |
| `status` | character varying | Y |
| `publish_at` | timestamp with time zone | Y |
| `failure_reason` | text |  |


### public.notification

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `target_id` | integer | Y |
| `title` | character varying |  |
| `body` | character varying |  |
| `image_url` | character varying |  |
| `is_read` | boolean | Y |
| `order_id` | integer |  |
| `type` | character varying | Y |
| `order_cancel_id` | integer |  |
| `play_id` | integer |  |
| `sender_id` | integer |  |
| `message_template` | character varying | Y |
| `data` | jsonb |  |


### public.notifications

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `user_id` | bigint | Y |
| `code` | character varying | Y |
| `notify_at` | timestamp with time zone | Y |
| `content` | text | Y |
| `is_sent` | timestamp with time zone |  |
| `is_read` | boolean |  |
| `sent_at` | timestamp with time zone |  |
| `metadata` | json |  |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone |  |


### public.performance

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `production_id` | bigint | Y |
| `theater_id` | bigint | Y |
| `date` | date | Y |
| `start_time` | time without time zone | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone |  |
| `source_key` | character varying |  |
| `is_special` | boolean | Y |


### public.performance_cast

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `performance_id` | bigint | Y |
| `cast_id` | bigint | Y |
| `character_name` | text |  |
| `role_type` | text |  |
| `order_index` | bigint |  |
| `data_source` | text |  |
| `created_at` | timestamp with time zone | Y |


### public.performance_user

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `user_id` | integer | Y |
| `performance_id` | bigint | Y |
| `custom_poster_media_id` | bigint | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone |  |


### public.post

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `content` | text | Y |
| `allow_comments` | boolean | Y |
| `visibility` | character varying | Y |
| `user_id` | integer | Y |
| `topic_id` | integer |  |
| `comment_count` | integer | Y |
| `like_count` | integer | Y |
| `view_count` | integer | Y |
| `share_count` | integer | Y |
| `is_pinned` | boolean | Y |
| `title` | text |  |
| `rating` | integer |  |
| `is_notification_enabled` | boolean | Y |


### public.post_media

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `mime_type` | character varying | Y |
| `url` | character varying | Y |
| `post_id` | integer | Y |


### public.post_reaction

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `user_id` | integer | Y |
| `post_id` | integer | Y |
| `type` | character varying | Y |


### public.post_report

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `status` | character varying | Y |
| `user_id` | integer | Y |
| `post_id` | integer | Y |
| `reason_id` | integer | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |


### public.post_views

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `post_id` | integer | Y |
| `user_id` | integer | Y |
| `created_at` | timestamp with time zone | Y |


### public.production

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `title` | text | Y |
| `genre` | text |  |
| `poster_media_id` | bigint |  |
| `description` | text |  |
| `opening_date` | date | Y |
| `closing_date` | date | Y |
| `running_time` | text |  |
| `created_at` | timestamp with time zone | Y |
| `theater_id` | bigint |  |
| `source_key` | character varying |  |
| `title_clean` | text |  |
| `title_canonical` | text |  |
| `title_location` | text |  |
| `title_suffix` | text |  |
| `title_canonical_compact` | text |  |
| `title_sort_group` | integer |  |
| `is_child` | boolean | Y |
| `genre_renew` | text |  |
| `updated_at` | timestamp with time zone |  |


### public.production_booking_site

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `production_id` | bigint | Y |
| `booking_site_id` | bigint | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone |  |


### public.production_booking_site_url

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `production_id` | bigint | Y |
| `booking_site_id` | bigint | Y |
| `url` | text | Y |
| `created_at` | timestamp with time zone | Y |


### public.production_edit_request

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `user_id` | bigint | Y |
| `production_id` | bigint |  |
| `performance_id` | bigint |  |
| `context` | text | Y |
| `status` | character varying | Y |
| `slack_sent` | boolean | Y |
| `slack_sent_at` | timestamp with time zone |  |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `reason_codes` | jsonb |  |


### public.production_seat_price

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `production_id` | bigint | Y |
| `seat_grade` | text | Y |
| `price` | bigint | Y |
| `created_at` | timestamp with time zone | Y |


### public.reason

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `label` | character varying | Y |
| `purpose` | character varying | Y |


### public.review

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `user_id` | integer | Y |
| `review_type` | character varying | Y |
| `target_id` | bigint | Y |
| `score` | numeric |  |
| `content` | text |  |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone |  |
| `deleted_at` | timestamp with time zone |  |


### public.review_media

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `review_id` | bigint | Y |
| `media_id` | bigint | Y |
| `order_index` | bigint |  |
| `created_at` | timestamp with time zone | Y |


### public.schema_migrations

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `version` | character varying | Y |


### public.search_history

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `user_id` | bigint |  |
| `keyword` | text | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |


### public.seat

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `theater_id` | bigint | Y |
| `floor` | character varying |  |
| `section` | character varying |  |
| `row` | character varying |  |
| `number` | bigint |  |
| `verification_count` | integer |  |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone |  |


### public.sub_genre

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `name` | character varying | Y |
| `genre_id` | integer | Y |


### public.tag

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `user_id` | bigint | Y |
| `name` | character varying | Y |
| `created_at` | timestamp with time zone | Y |
| `production_id` | bigint | Y |


### public.theater

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `venue_id` | bigint |  |
| `name` | text |  |
| `capacity` | bigint |  |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone |  |
| `source_key` | character varying |  |


### public.ticket

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `user_id` | integer | Y |
| `performance_id` | bigint | Y |
| `booking_site_id` | bigint |  |
| `seat_id` | bigint |  |
| `seat_grade` | character varying |  |
| `price` | bigint |  |
| `ticket_type` | character varying |  |
| `is_transfer` | boolean |  |
| `booking_receipt_media_id` | bigint |  |
| `public_type` | character varying |  |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone |  |
| `deleted_at` | timestamp with time zone |  |


### public.ticket_book

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `user_id` | integer | Y |
| `play_date` | date | Y |
| `play_time` | time without time zone |  |
| `seat_name` | character varying |  |
| `seat_grade_name` | character varying |  |
| `seat_price` | integer |  |
| `rating` | numeric |  |
| `review` | text |  |
| `topic_play_id` | integer | Y |
| `is_pinned` | boolean | Y |


### public.ticket_book_image

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `ticket_book_id` | integer | Y |
| `url` | character varying | Y |


### public.ticket_book_media

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `mime_type` | character varying | Y |
| `url` | character varying | Y |
| `ticket_book_id` | integer | Y |


### public.ticket_book_performance_mapping

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `ticket_book_id` | integer | Y |
| `performance_id` | bigint | Y |
| `notes` | text |  |
| `created_at` | timestamp without time zone |  |


### public.ticket_cast

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `ticket_id` | bigint | Y |
| `cast_id` | bigint |  |
| `cast_name` | character varying | Y |
| `character_name` | character varying |  |
| `is_custom` | boolean |  |
| `order_index` | bigint |  |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone |  |


### public.ticket_parsing_log

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `user_id` | integer | Y |
| `request_timestamp` | timestamp with time zone | Y |
| `html_input` | text |  |
| `html_size_bytes` | integer | Y |
| `input_tokens` | integer |  |
| `output_tokens` | integer |  |
| `response_timestamp` | timestamp with time zone |  |
| `response_time_ms` | integer |  |
| `model` | character varying | Y |
| `status` | character varying | Y |
| `parsed_data` | jsonb |  |
| `error_message` | text |  |
| `performance_id` | bigint |  |
| `matching_score` | numeric |  |
| `ticket_id` | bigint |  |
| `ticket_creation_status` | character varying | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |


### public.ticket_status_log

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `ticket_id` | integer | Y |
| `from_payment_status` | character varying | Y |
| `to_payment_status` | character varying | Y |
| `from_issuance_status` | character varying | Y |
| `to_issuance_status` | character varying | Y |
| `changed_by` | character varying |  |


### public.ticket_verification

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `image_url` | character varying | Y |
| `status` | character varying | Y |
| `rejected_reason` | text |  |
| `ticket_book_id` | integer | Y |
| `is_read_result` | boolean | Y |


### public.topic

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `name` | character varying | Y |
| `image_url` | character varying |  |
| `post_count` | integer | Y |
| `genre_id` | integer |  |


### public.topic_follow

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `user_id` | integer | Y |
| `topic_id` | integer | Y |


### public.topic_play

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `play_name` | character varying | Y |
| `place_name` | character varying | Y |
| `topic_id` | integer | Y |
| `image_url` | character varying |  |


### public.user

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `uuid` | character varying | Y |
| `profile_image_url` | character varying |  |
| `nickname` | character varying | Y |
| `is_marketing_agreed` | boolean | Y |
| `marketing_agreed_at` | timestamp with time zone |  |
| `is_auto_play_video_on_wifi_only` | boolean | Y |
| `username` | character varying | Y |
| `bio` | text |  |
| `is_newsletter_alert_enabled` | boolean | Y |
| `is_post_like_alert_enabled` | boolean | Y |
| `is_post_comment_alert_enabled` | boolean | Y |
| `is_comment_like_alert_enabled` | boolean | Y |
| `is_comment_reply_alert_enabled` | boolean | Y |
| `is_follow_request_alert_enabled` | boolean | Y |
| `is_following_user_post_alert_enabled` | boolean | Y |
| `is_following_user_ticketbook_alert_enabled` | boolean | Y |
| `is_following_topic_post_alert_enabled` | boolean | Y |
| `is_ticket_verification_alert_enabled` | boolean | Y |
| `is_ticket_verification_suggest_alert_enabled` | boolean | Y |
| `theme` | character varying | Y |
| `is_notification_enabled` | boolean | Y |
| `is_play_day_notification_enabled` | boolean | Y |
| `is_play_entry_notification_enabled` | boolean | Y |
| `is_ticket_book_after_play_notification_enabled` | boolean | Y |
| `is_play_open_notification_enabled` | boolean | Y |
| `is_casting_update_notification_enabled` | boolean | Y |
| `is_related_content_upload_notification_enabled` | boolean | Y |
| `is_notice_notification_enabled` | boolean | Y |
| `is_coupon_notification_enabled` | boolean | Y |
| `is_event_notification_enabled` | boolean | Y |
| `last_access_at` | timestamp with time zone | Y |
| `status` | character varying | Y |
| `nickname_change_count` | integer | Y |
| `nickname_change_window_started_at` | timestamp with time zone |  |


### public.user_auth_email

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `email` | character varying | Y |
| `password` | character varying | Y |
| `user_id` | integer | Y |


### public.user_auth_social

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `user_id` | integer | Y |
| `provider` | character varying | Y |
| `provider_user_id` | character varying | Y |
| `email` | character varying |  |
| `profile_image_url` | character varying |  |


### public.user_block

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `user_id` | integer | Y |
| `target_id` | integer | Y |
| `deleted_at` | timestamp with time zone |  |


### public.user_delete_reason

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `user_id` | integer | Y |
| `reason_id` | integer | Y |
| `reason_detail` | character varying |  |


### public.user_fcm_token

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `user_id` | integer | Y |
| `fcm_token` | character varying | Y |
| `device_type` | character varying |  |
| `device_model` | character varying |  |
| `is_active` | boolean | Y |


### public.user_follow

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `user_id` | integer | Y |
| `target_id` | integer | Y |


### public.user_hidden_comments

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `user_id` | bigint | Y |
| `comment_id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |


### public.user_hidden_posts

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `user_id` | bigint | Y |
| `post_id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |


### public.user_identity_verification_history

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `user_id` | integer | Y |
| `expired_at` | timestamp with time zone | Y |


### public.user_pass_identity

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |
| `name` | character varying | Y |
| `birthdate` | character varying | Y |
| `sex` | character varying | Y |
| `ntv_frnr` | character varying | Y |
| `di` | character varying | Y |
| `ci` | character varying | Y |
| `tel_com` | character varying | Y |
| `tel_no` | character varying | Y |
| `user_id` | integer | Y |


### public.user_report

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `status` | character varying | Y |
| `user_id` | integer | Y |
| `target_id` | integer | Y |
| `reason_id` | integer | Y |
| `updated_at` | timestamp with time zone | Y |
| `deleted_at` | timestamp with time zone |  |


### public.user_suspension_history

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | integer | Y |
| `created_at` | timestamp with time zone | Y |
| `user_id` | integer | Y |
| `reason_id` | integer | Y |
| `suspended_days` | integer |  |
| `revoked_at` | timestamp without time zone |  |


### public.venue

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `name` | text | Y |
| `address` | text |  |
| `created_at` | timestamp with time zone | Y |
| `updated_at` | timestamp with time zone |  |
| `source_key` | character varying |  |
| `name_clean` | text |  |


---

## kopis 스키마 (공연예술통합전산망)


### kopis.facility

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `mt10id` | character varying | Y |
| `fcltynm` | text |  |
| `mt13cnt` | smallint |  |
| `fcltychartr` | text |  |
| `opende` | smallint |  |
| `seatscale` | integer |  |
| `telno` | text |  |
| `relateurl` | text |  |
| `adres` | text |  |
| `la` | double precision |  |
| `lo` | double precision |  |
| `restaurant` | character |  |
| `cafe` | character |  |
| `store` | character |  |
| `nolibang` | character |  |
| `suyu` | character |  |
| `parkbarrier` | character |  |
| `restbarrier` | character |  |
| `runwbarrier` | character |  |
| `elevbarrier` | character |  |
| `parkinglot` | character |  |
| `created_at` | timestamp with time zone |  |
| `updated_at` | timestamp with time zone |  |


### kopis.facility_list

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `mt10id` | character varying | Y |
| `fcltynm` | text |  |
| `mt13cnt` | smallint |  |
| `fcltychartr` | text |  |
| `sidonm` | text |  |
| `gugunnm` | text |  |
| `opende` | smallint |  |
| `created_at` | timestamp with time zone |  |
| `updated_at` | timestamp with time zone |  |


### kopis.kopis_ingest_history

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `source_table` | character varying | Y |
| `source_id` | character varying | Y |
| `action_type` | character varying | Y |
| `source_hash` | character varying | Y |
| `hash_version` | integer | Y |
| `created_at` | timestamp with time zone | Y |


### kopis.marker

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `task_name` | character varying | Y |
| `task_params` | jsonb | Y |
| `status` | character varying | Y |
| `processed_count` | integer | Y |
| `processed_page` | integer |  |
| `message` | text |  |
| `started_at` | timestamp with time zone | Y |
| `finished_at` | timestamp with time zone |  |
| `created_at` | timestamp with time zone |  |
| `updated_at` | timestamp with time zone |  |


### kopis.performance

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `mt20id` | character varying | Y |
| `prfnm` | text |  |
| `prfpdfrom` | date |  |
| `prfpdto` | date |  |
| `fcltynm` | text |  |
| `mt10id` | character varying |  |
| `prfcast` | text |  |
| `prfcrew` | text |  |
| `prfruntime` | text |  |
| `prfage` | text |  |
| `entrpsnm` | text |  |
| `entrpsnmP` | text |  |
| `entrpsnmA` | text |  |
| `entrpsnmH` | text |  |
| `entrpsnmS` | text |  |
| `pcseguidance` | text |  |
| `poster` | text |  |
| `sty` | text |  |
| `area` | text |  |
| `genrenm` | text |  |
| `openrun` | character |  |
| `visit` | character |  |
| `child` | character |  |
| `daehakro` | character |  |
| `festival` | character |  |
| `musicallicense` | character |  |
| `musicalcreate` | character |  |
| `updatedate` | timestamp without time zone |  |
| `prfstate` | text |  |
| `dtguidance` | text |  |
| `created_at` | timestamp with time zone |  |
| `updated_at` | timestamp with time zone |  |


### kopis.performance_list

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `mt20id` | character varying | Y |
| `prfnm` | text |  |
| `prfpdfrom` | date |  |
| `prfpdto` | date |  |
| `fcltynm` | text |  |
| `poster` | text |  |
| `area` | text |  |
| `genrenm` | text |  |
| `openrun` | character |  |
| `prfstate` | character varying |  |
| `created_at` | timestamp with time zone |  |
| `updated_at` | timestamp with time zone |  |


### kopis.performance_place

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `mt10id` | character varying |  |
| `prfplcnm` | text |  |
| `mt13id` | character varying |  |
| `seatscale` | text |  |
| `stageorchat` | character |  |
| `stagepracat` | character |  |
| `stagedresat` | character |  |
| `stageoutdrat` | character |  |
| `disabledseatscale` | text |  |
| `stagearea` | text |  |
| `created_at` | timestamp with time zone |  |
| `updated_at` | timestamp with time zone |  |


### kopis.relate

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `mt20id` | character varying |  |
| `relatenm` | text |  |
| `relateurl` | text |  |
| `created_at` | timestamp with time zone |  |
| `updated_at` | timestamp with time zone |  |


### kopis.transformation_progress

| 컬럼명 | 타입 | NOT NULL |
|--------|------|----------|
| `id` | bigint | Y |
| `source_table` | character varying | Y |
| `source_id` | character varying | Y |
| `target_table` | character varying | Y |
| `target_id` | bigint | Y |
| `created_at` | timestamp with time zone | Y |
| `action_type` | character varying |  |
| `source_hash` | character varying |  |
| `hash_version` | integer |  |
