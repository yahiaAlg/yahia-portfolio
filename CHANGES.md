# What's in this bundle

Drop these files into your repo at the same relative paths (they overwrite/add to `pages/`), then run:

```bash
python manage.py migrate
python manage.py seed_portfolio
```

## Files

- **pages/models.py** — added `blank=True` to every `order` field (Certification, ContactLink,
  Experience, Language, Project, Skill, SkillCategory, TrainingCourse). They had `default=0` but
  not `blank=True`, so Django admin forms still marked them "required" — most noticeable as
  spurious "This field is required" errors on the Skill inline rows under Skill Category.

- **pages/admin.py** — restored a `cert_thumb` preview column on `CertificationAdmin` (it was
  dropped in an earlier refactor), so you can see certificate images at a glance in the list view.

- **pages/migrations/0006_alter_certification_order_alter_contactlink_order_and_more.py** —
  migration for the `blank=True` model changes above. Just run `migrate`.

- **pages/management/commands/seed_portfolio.py** — updated:
  - Honorary Teacher (Vacataire) experience: end date now `May 2026` instead of `Present`.
  - New experience: **System Administrator, Developer & Trainer** @ EEMS — Excellence Management
    Solutions, Sétif, start `Mar 2026`, ongoing. Covers Windows/Ubuntu Server admin, PostgreSQL/MySQL +
    backup strategy, Bash/PowerShell automation, web dev + hardware maintenance, networking
    (routing, port forwarding, OpenVPN), and your Formateur/trainer work.
  - New certification: **English Certificate — B2.1**, CEIL/Université Ferhat Abbas Sétif 1,
    dated `19/03/2026` (read off your certificate — it's March, not May).
  - Switched `Experience` and `Certification` seeding from `get_or_create` to `update_or_create`,
    so re-running the seed command actually applies edits to existing rows instead of silently
    skipping them (this is what would've eaten the "Present → May 2026" change otherwise).
  - Added `_attach_asset_image()`, which auto-attaches a bundled image to a Certification's
    `image` field on seed if it doesn't have one yet — no manual admin upload needed for the new cert.

- **pages/seed_assets/certifications/certificat_english_b2_lakhfif.png** — your English B2.1
  certificate, extracted from the PDF and rotated right-side-up, referenced by the seed script above.
