# Moneypenny: hosted AOL reviewer

Deployment-ready starter, not installed or connected. This is separate from the Gmail/Outlook automation already named Moneypenny in ChatGPT.

## What it does
Reads AOL folders (including Sent, excluding Trash/Junk/Drafts) over encrypted IMAP, sends message text to OpenAI for analysis, and sends the recap from your AOL address to your Gmail address. It never sends replies to contacts or alters the AOL mailbox. Recap email is its only write action. Attachments are not analyzed. It produces a fresh 30-calendar-day scan each run, not a persistent completed-task database.

Default schedule: weekdays around 6:30 a.m. America/New_York, ahead of your 7 a.m. ChatGPT recap. Late delivery can miss the 7 a.m. run. No automatic data connection to ChatGPT: its existing Gmail review can find the delivered email. Do not forward the recap back to AOL in a loop.

## Setup from Windows
1. Extract this ZIP. Create a private GitHub repository and upload the contents of this folder to its root (moneypenny.py, Dockerfile, render.yaml, and these instructions). Never upload passwords or keys.
2. Sign in at https://dashboard.render.com and choose New > Blueprint. Connect that private repository. Review the service and billing before deploying. This creates one paid cron job.
3. Enter these private environment values when prompted:
   - AOL_EMAIL: your full AOL address.
   - AOL_APP_PASSWORD: an AOL-generated app password, not your normal login password.
   - OPENAI_API_KEY: a key from https://platform.openai.com/api-keys with funded API access.
   - RECAP_TO: wjeff.cartwright@gmail.com (verify this is your intended destination).
4. Deploy. For the first controlled test, set the service's Docker Command to `python -u moneypenny.py --force --dry-run`, save/redeploy, and Trigger Run. This reads AOL and incurs an AI API request but does not send the recap. A success message confirms analysis worked; no email bodies or credentials are printed in logs.
5. To deliver your first recap now, change Docker Command to `python -u moneypenny.py --force`, save/redeploy, and Trigger Run once. Check Gmail (including Spam). Avoid triggering a new run while one is already active.
6. IMPORTANT: Restore Docker Command to `python -u moneypenny.py` after testing. Leaving `--force` on would cause two daily recaps. Normal schedule triggers at 10:30 and 11:30 UTC; the application allows only the weekday 6:30-6:59 a.m. Eastern run, automatically accounting for daylight saving time.

## Cost and privacy
Render documents a $1 minimum per cron job per month; usage may cost more. OpenAI API usage is separate from ChatGPT subscription billing. See current prices before deployment. This starter makes one AI request per accepted run and rescans the configured window. Costs depend on message volume; there is no guaranteed monthly cap in this code. It fails before analysis if the input exceeds 1.2 million JSON characters.

The hosting provider processes credentials and email text; OpenAI receives email headers/body excerpts for analysis; the Gmail recipient receives the result. `store:false` is set on the API request, but that is not a promise of zero retention. Use the providers' applicable data policies. No email attachments are uploaded. Credentials are read only from environment settings, never embedded in the repository.

## Coverage and limitations
- Newest 250 messages per folder by default. Any skipped messages, unreadable folders, or truncated bodies are disclosed in the recap. Increase MAX_MESSAGES_PER_FOLDER (up to 1000) or reduce LOOKBACK_DAYS if needed, considering API cost.
- Each body is capped at 4,000 characters; older quoted text can be truncated. A newer reply may resolve an older request, so review items marked Confirm status.
- Archived/custom folders are included when selectable; unfamiliar mailbox naming/permissions may need adaptation. Folder identifiers may appear encoded for non-English names.
- No completion tracking beyond information in the scanned email. Work done by phone, text, or outside the window can still appear unresolved.
- Model output is advisory. No financial transfers, mailbox deletion, external link fetching, or attachment opening occurs.
- Delivery is not guaranteed exactly once: manually rerunning after delivery can duplicate a recap. The app does not automatically retry SMTP sends.
- If a job fails, inspect its Render Runs status. No successful recap is sent if reading/analysis fails. Configure failure notifications in your host account where available.
- Pause the cron job in Render to stop it. Revoke credentials in AOL/OpenAI if retiring it.

## Verification
Local parsing, schedule logic (summer/winter), and read-only IMAP operations are tested with synthetic data. Actual AOL authentication, Render hosting/network access, AI API access, and email delivery require your account setup and have not been live-tested.

## Official references
AOL settings: https://help.aol.com/articles/how-do-i-use-other-email-applications-to-send-and-receive-my-aol-mail
AOL app passwords: https://help.aol.com/articles/create-and-manage-app-password
Render cron jobs/billing: https://render.com/docs/cronjobs
Render Blueprint configuration: https://render.com/docs/blueprint-spec
OpenAI text generation: https://developers.openai.com/api/docs/guides/text
OpenAI API pricing: https://developers.openai.com/api/docs/pricing
