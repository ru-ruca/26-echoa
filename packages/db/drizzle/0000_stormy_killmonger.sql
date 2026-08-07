CREATE TYPE "public"."content_origin" AS ENUM('self_authored', 'ai_generated', 'ai_rewritten', 'public_domain');--> statement-breakpoint
CREATE TABLE "account" (
	"id" text PRIMARY KEY NOT NULL,
	"user_id" text NOT NULL,
	"account_id" text NOT NULL,
	"provider_id" text NOT NULL,
	"access_token" text,
	"refresh_token" text,
	"access_token_expires_at" timestamp,
	"refresh_token_expires_at" timestamp,
	"scope" text,
	"id_token" text,
	"password" text,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "session" (
	"id" text PRIMARY KEY NOT NULL,
	"user_id" text NOT NULL,
	"token" text NOT NULL,
	"expires_at" timestamp NOT NULL,
	"ip_address" text,
	"user_agent" text,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "session_token_unique" UNIQUE("token")
);
--> statement-breakpoint
CREATE TABLE "user" (
	"id" text PRIMARY KEY NOT NULL,
	"name" text NOT NULL,
	"email" text NOT NULL,
	"email_verified" boolean DEFAULT false NOT NULL,
	"image" text,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "user_email_unique" UNIQUE("email")
);
--> statement-breakpoint
CREATE TABLE "verification" (
	"id" text PRIMARY KEY NOT NULL,
	"identifier" text NOT NULL,
	"value" text NOT NULL,
	"expires_at" timestamp NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "collocations" (
	"id" serial PRIMARY KEY NOT NULL,
	"phrase" text NOT NULL,
	"base_word" text NOT NULL,
	"collocation_type" text,
	"cefr_level" text,
	"meaning_kr" text,
	"example_en" text,
	"example_kr" text,
	"frequency_rank" integer,
	"source" text DEFAULT 'ai_generated' NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "expressions" (
	"id" serial PRIMARY KEY NOT NULL,
	"expression" text NOT NULL,
	"type" text,
	"meaning_kr" text,
	"cefr_level" text,
	"example1_en" text,
	"example1_kr" text,
	"example2_en" text,
	"example2_kr" text,
	"created_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "intonation_patterns" (
	"id" serial PRIMARY KEY NOT NULL,
	"pattern_name" text NOT NULL,
	"description_kr" text,
	"visual_notation" text,
	"example_sentence_ids" jsonb,
	"audio_url" text,
	"created_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "intonation_patterns_pattern_name_unique" UNIQUE("pattern_name")
);
--> statement-breakpoint
CREATE TABLE "morphemes" (
	"id" serial PRIMARY KEY NOT NULL,
	"morpheme" text NOT NULL,
	"type" text NOT NULL,
	"meaning_kr" text,
	"meaning_en" text,
	"origin" text,
	"examples" jsonb,
	"frequency_rank" integer,
	"created_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "morphemes_morpheme_unique" UNIQUE("morpheme")
);
--> statement-breakpoint
CREATE TABLE "sentence_ipa" (
	"id" serial PRIMARY KEY NOT NULL,
	"sentence_id" text NOT NULL,
	"ipa_full" text,
	"ipa_chunks" jsonb,
	"stress_words" jsonb,
	"intonation_pattern_id" integer,
	"tts_speed" numeric DEFAULT '1.0' NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "sentence_ipa_sentence_id_unique" UNIQUE("sentence_id")
);
--> statement-breakpoint
CREATE TABLE "sentence_words" (
	"id" serial PRIMARY KEY NOT NULL,
	"sentence_id" text NOT NULL,
	"word_id" text NOT NULL,
	"word_text" text,
	"created_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "sentences" (
	"id" text PRIMARY KEY NOT NULL,
	"month" integer NOT NULL,
	"week" integer NOT NULL,
	"day" integer NOT NULL,
	"day_type" text,
	"text_en" text NOT NULL,
	"text_kr" text NOT NULL,
	"cefr_level" text,
	"content_origin" "content_origin" NOT NULL,
	"source_id" integer,
	"stress_pattern" text,
	"is_new" boolean DEFAULT true NOT NULL,
	"notes" text,
	"audio_url" text,
	"chunk_breaks" jsonb,
	"speaking_duration_sec" numeric,
	"intonation_pattern_id" integer,
	"dialogue_id" text,
	"speaker" text,
	"dialogue_title" text,
	"dialogue_situation" text,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "sources" (
	"id" serial PRIMARY KEY NOT NULL,
	"source_type" text,
	"title" text,
	"author" text,
	"year" integer,
	"url" text,
	"created_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "vocabulary" (
	"id" text PRIMARY KEY NOT NULL,
	"word" text NOT NULL,
	"pos" text,
	"cefr_level" text,
	"meaning_kr" text,
	"pronunciation" text,
	"pronunciation_kr" text,
	"examples" jsonb,
	"first_month" integer,
	"syllable_breakdown" text,
	"syllable_count" integer,
	"primary_stress_position" integer,
	"secondary_stress_position" integer,
	"audio_url" text,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "vocabulary_morphemes" (
	"vocabulary_id" text NOT NULL,
	"morpheme_id" integer NOT NULL,
	"position" text,
	"order_index" integer DEFAULT 1 NOT NULL,
	CONSTRAINT "vocabulary_morphemes_vocabulary_id_morpheme_id_pk" PRIMARY KEY("vocabulary_id","morpheme_id")
);
--> statement-breakpoint
CREATE TABLE "badges" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" text NOT NULL,
	"description_kr" text NOT NULL,
	"icon" text NOT NULL,
	"condition_type" text NOT NULL,
	"condition_value" integer NOT NULL,
	"bonus_xp" integer DEFAULT 0 NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "badges_name_unique" UNIQUE("name")
);
--> statement-breakpoint
CREATE TABLE "favorites" (
	"id" serial PRIMARY KEY NOT NULL,
	"user_id" text NOT NULL,
	"word_id" text NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "user_badges" (
	"id" serial PRIMARY KEY NOT NULL,
	"user_id" text NOT NULL,
	"badge_id" integer NOT NULL,
	"earned_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "user_progress" (
	"id" serial PRIMARY KEY NOT NULL,
	"user_id" text NOT NULL,
	"item_type" text NOT NULL,
	"item_id" text NOT NULL,
	"correct_count" integer DEFAULT 0 NOT NULL,
	"wrong_count" integer DEFAULT 0 NOT NULL,
	"last_reviewed_at" timestamp,
	"next_review_at" timestamp,
	"fsrs_difficulty" real DEFAULT 0,
	"fsrs_stability" real DEFAULT 0,
	"fsrs_elapsed_days" integer DEFAULT 0,
	"fsrs_scheduled_days" integer DEFAULT 0,
	"fsrs_reps" integer DEFAULT 0,
	"fsrs_lapses" integer DEFAULT 0,
	"fsrs_state" integer DEFAULT 0,
	"fsrs_last_review" timestamp,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "user_streaks" (
	"id" serial PRIMARY KEY NOT NULL,
	"user_id" text NOT NULL,
	"current_streak" integer DEFAULT 0 NOT NULL,
	"longest_streak" integer DEFAULT 0 NOT NULL,
	"last_study_date" text,
	"freeze_available_at" timestamp,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "user_streaks_user_id_unique" UNIQUE("user_id")
);
--> statement-breakpoint
CREATE TABLE "user_xp" (
	"id" serial PRIMARY KEY NOT NULL,
	"user_id" text NOT NULL,
	"total_xp" integer DEFAULT 0 NOT NULL,
	"daily_xp" integer DEFAULT 0 NOT NULL,
	"daily_xp_date" text,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "user_xp_user_id_unique" UNIQUE("user_id")
);
--> statement-breakpoint
CREATE TABLE "xp_history" (
	"id" serial PRIMARY KEY NOT NULL,
	"user_id" text NOT NULL,
	"xp_amount" integer NOT NULL,
	"source" text NOT NULL,
	"item_type" text,
	"item_id" text,
	"created_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "content_originals" (
	"id" serial PRIMARY KEY NOT NULL,
	"sentence_id" text NOT NULL,
	"original_text_en" text NOT NULL,
	"original_text_kr" text,
	"source_id" integer,
	"rewrite_meta" jsonb,
	"created_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "content_originals_sentence_id_unique" UNIQUE("sentence_id")
);
--> statement-breakpoint
ALTER TABLE "account" ADD CONSTRAINT "account_user_id_user_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."user"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "session" ADD CONSTRAINT "session_user_id_user_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."user"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "sentence_ipa" ADD CONSTRAINT "sentence_ipa_sentence_id_sentences_id_fk" FOREIGN KEY ("sentence_id") REFERENCES "public"."sentences"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "sentence_ipa" ADD CONSTRAINT "sentence_ipa_intonation_pattern_id_intonation_patterns_id_fk" FOREIGN KEY ("intonation_pattern_id") REFERENCES "public"."intonation_patterns"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "sentence_words" ADD CONSTRAINT "sentence_words_sentence_id_sentences_id_fk" FOREIGN KEY ("sentence_id") REFERENCES "public"."sentences"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "sentence_words" ADD CONSTRAINT "sentence_words_word_id_vocabulary_id_fk" FOREIGN KEY ("word_id") REFERENCES "public"."vocabulary"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "sentences" ADD CONSTRAINT "sentences_source_id_sources_id_fk" FOREIGN KEY ("source_id") REFERENCES "public"."sources"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "sentences" ADD CONSTRAINT "sentences_intonation_pattern_id_intonation_patterns_id_fk" FOREIGN KEY ("intonation_pattern_id") REFERENCES "public"."intonation_patterns"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "vocabulary_morphemes" ADD CONSTRAINT "vocabulary_morphemes_vocabulary_id_vocabulary_id_fk" FOREIGN KEY ("vocabulary_id") REFERENCES "public"."vocabulary"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "vocabulary_morphemes" ADD CONSTRAINT "vocabulary_morphemes_morpheme_id_morphemes_id_fk" FOREIGN KEY ("morpheme_id") REFERENCES "public"."morphemes"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "favorites" ADD CONSTRAINT "favorites_user_id_user_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."user"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "favorites" ADD CONSTRAINT "favorites_word_id_vocabulary_id_fk" FOREIGN KEY ("word_id") REFERENCES "public"."vocabulary"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "user_badges" ADD CONSTRAINT "user_badges_user_id_user_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."user"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "user_badges" ADD CONSTRAINT "user_badges_badge_id_badges_id_fk" FOREIGN KEY ("badge_id") REFERENCES "public"."badges"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "user_progress" ADD CONSTRAINT "user_progress_user_id_user_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."user"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "user_streaks" ADD CONSTRAINT "user_streaks_user_id_user_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."user"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "user_xp" ADD CONSTRAINT "user_xp_user_id_user_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."user"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "xp_history" ADD CONSTRAINT "xp_history_user_id_user_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."user"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "content_originals" ADD CONSTRAINT "content_originals_sentence_id_sentences_id_fk" FOREIGN KEY ("sentence_id") REFERENCES "public"."sentences"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "content_originals" ADD CONSTRAINT "content_originals_source_id_sources_id_fk" FOREIGN KEY ("source_id") REFERENCES "public"."sources"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "idx_collocations_base_word" ON "collocations" USING btree ("base_word");--> statement-breakpoint
CREATE INDEX "idx_collocations_cefr" ON "collocations" USING btree ("cefr_level");--> statement-breakpoint
CREATE INDEX "idx_morphemes_type" ON "morphemes" USING btree ("type");--> statement-breakpoint
CREATE INDEX "idx_sentence_ipa_sentence" ON "sentence_ipa" USING btree ("sentence_id");--> statement-breakpoint
CREATE INDEX "idx_sentence_words_sentence_id" ON "sentence_words" USING btree ("sentence_id");--> statement-breakpoint
CREATE INDEX "idx_sentence_words_word_id" ON "sentence_words" USING btree ("word_id");--> statement-breakpoint
CREATE UNIQUE INDEX "sentence_words_unique" ON "sentence_words" USING btree ("sentence_id","word_id");--> statement-breakpoint
CREATE INDEX "idx_sentences_month" ON "sentences" USING btree ("month");--> statement-breakpoint
CREATE INDEX "idx_sentences_week" ON "sentences" USING btree ("week");--> statement-breakpoint
CREATE INDEX "idx_sentences_day" ON "sentences" USING btree ("day");--> statement-breakpoint
CREATE INDEX "idx_sentences_day_type" ON "sentences" USING btree ("day_type");--> statement-breakpoint
CREATE INDEX "idx_sentences_dialogue_id" ON "sentences" USING btree ("dialogue_id");--> statement-breakpoint
CREATE INDEX "idx_sentences_content_origin" ON "sentences" USING btree ("content_origin");--> statement-breakpoint
CREATE INDEX "idx_vocabulary_word" ON "vocabulary" USING btree ("word");--> statement-breakpoint
CREATE INDEX "idx_vocabulary_cefr_level" ON "vocabulary" USING btree ("cefr_level");--> statement-breakpoint
CREATE INDEX "idx_favorites_user" ON "favorites" USING btree ("user_id");--> statement-breakpoint
CREATE INDEX "idx_favorites_word" ON "favorites" USING btree ("word_id");--> statement-breakpoint
CREATE UNIQUE INDEX "favorites_user_word_unique" ON "favorites" USING btree ("user_id","word_id");--> statement-breakpoint
CREATE INDEX "idx_user_badges_user" ON "user_badges" USING btree ("user_id");--> statement-breakpoint
CREATE UNIQUE INDEX "user_badges_user_badge_unique" ON "user_badges" USING btree ("user_id","badge_id");--> statement-breakpoint
CREATE INDEX "idx_user_progress_user" ON "user_progress" USING btree ("user_id");--> statement-breakpoint
CREATE INDEX "idx_user_progress_next_review" ON "user_progress" USING btree ("user_id","next_review_at");--> statement-breakpoint
CREATE UNIQUE INDEX "user_progress_user_item_unique" ON "user_progress" USING btree ("user_id","item_type","item_id");--> statement-breakpoint
CREATE INDEX "idx_user_streaks_user" ON "user_streaks" USING btree ("user_id");--> statement-breakpoint
CREATE INDEX "idx_user_xp_user" ON "user_xp" USING btree ("user_id");--> statement-breakpoint
CREATE INDEX "idx_xp_history_user" ON "xp_history" USING btree ("user_id");--> statement-breakpoint
CREATE INDEX "idx_xp_history_date" ON "xp_history" USING btree ("user_id","created_at");--> statement-breakpoint
CREATE INDEX "idx_content_originals_sentence" ON "content_originals" USING btree ("sentence_id");