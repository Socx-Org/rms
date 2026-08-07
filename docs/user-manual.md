# RMS User Manual

**Reminder Management System** — a platform for scheduling and sending reminders to event subscribers via email and SMS.

---

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Managing Events](#2-managing-events)
3. [Reminders](#3-reminders)
4. [Subscribers](#4-subscribers)
5. [Access Management](#5-access-management)
6. [Reports](#6-reports)

---

## 1. Getting Started

### Create an Account

1. Navigate to the app and click **Register**.
2. Fill in your first name, last name, email address, password, and preferred timezone.
3. Submit the form — a verification email will be sent to your address.
4. Open the email and click the verification link to activate your account.

> If the verification email does not arrive, use the **Resend verification** link on the login page.

### Log In

1. Go to the **Login** page.
2. Enter your email and password and submit.
3. You will be taken to your events list.

---

## 2. Managing Events

### Creating an Event

1. From your **Events** list, click **+ New event**.
2. Fill in the form:

   | Field | Required | Notes |
   |-------|----------|-------|
   | Subject | Yes | The title of the event |
   | Date & time | Yes | When the event occurs |
   | Timezone | Yes | Pre-filled from your browser; accepts any IANA timezone e.g. `Europe/London` |
   | Location | No | A free-text venue or room name |
   | Description | No | Optional notes |

3. Click **Create event**. The new event appears in your list with an **Owner** badge and **Active** status.

### Viewing and Editing an Event

Click any event in the list to open its detail page. The page has four tabs:

- **Details** — view or edit the event's core fields (owner + active events only)
- **Reminders** — manage scheduled reminders
- **Subscribers** — manage the people who will receive reminders
- **Access** — manage collaborator access *(owner only)*

To edit event details, make changes in the Details tab and click **Save changes**.

### Filtering Events

The events list can be filtered by role and status using the pill buttons above the list:

- **All** — shows everything you have access to
- **Mine** — events you own
- **Shared** — events shared with you by another owner
- **Active / Cancelled / Archived** — filter by event status

### Cancelling an Event

On the Events list, click **Cancel** next to an event. This cannot be undone.

---

## 3. Reminders

Reminders are scheduled notifications sent to all active subscribers. They can be sent via **email**, **SMS**, or both. An event can have up to **5 reminders**.

> **Who can manage reminders?**  
> Owners and Contributors can add and edit reminders. Only the Owner can cancel (delete) a reminder.

### Opening the Reminders Tab

1. Open an event's detail page.
2. Click the **Reminders** tab.

### Adding a Reminder

1. Click **+ Add reminder**.
2. Fill in the form:

   | Field | Required | Notes |
   |-------|----------|-------|
   | Remind at | Yes | The date and time the first notification is sent |
   | Subject template | Yes | The notification subject line. You can use `{{event_subject}}` as a variable |
   | Body template | Yes | The notification body. HTML is supported. Use `{{subscriber_firstname}}` to personalise |
   | Channels | Yes | Tick **Email**, **SMS**, or both |
   | Recurrence | No | How often the reminder repeats after the first send (default: Never) |

3. Click **Add reminder**. The reminder appears in the list with a **Scheduled** status badge.

#### Template Variables

| Variable | Replaced with |
|----------|---------------|
| `{{event_subject}}` | The event's subject/title |
| `{{subscriber_firstname}}` | The subscriber's first name |
| `{{subscriber_lastname}}` | The subscriber's last name |

#### Recurrence Options

| Option | Behaviour |
|--------|-----------|
| Never (one-time) | Sends once at the scheduled time |
| Hourly | Repeats every hour |
| Daily | Repeats every day |
| Weekdays (Mon–Fri) | Repeats on working days |
| Weekends (Sat–Sun) | Repeats on Saturday and Sunday |
| Weekly | Repeats every 7 days |
| Fortnightly | Repeats every 14 days |
| Monthly | Repeats on the same day each month |
| Every 3 months | Repeats quarterly |
| Every 6 months | Repeats twice a year |
| Yearly | Repeats annually |

### Reminder Statuses

| Status | Meaning |
|--------|---------|
| **Scheduled** | Waiting to be sent |
| **Processing** | Currently being dispatched |
| **Recurring** | Has sent at least once and will send again |
| **Sent** | Sent and completed (non-recurring) |
| **Cancelled** | Manually cancelled by the owner |
| **Failed** | Dispatch failed |

### Editing a Reminder

1. In the Reminders tab, click **Edit** next to the reminder.
2. Update any field.
3. Click **Save changes**.

> Reminders with status **Recurring**, **Sent**, **Cancelled**, or **Failed** cannot be edited.

### Previewing a Reminder

When editing an existing reminder, click **Preview occurrence** at the bottom-left of the form. This renders the subject and body templates using the first subscriber found for the event, and shows the next scheduled send time.

### Cancelling a Reminder

Cancelling a reminder stops future sends. Only the event owner can cancel.

1. Click **Cancel** next to the reminder.
2. Confirm by clicking **Cancel reminder** in the dialog.

> If a reminder is already being processed, cancellation will still stop any future recurrences but cannot recall messages already dispatched.

---

## 4. Subscribers

Subscribers are the people who receive reminders when they are sent. Each subscriber must have at least one **contact** (email address or phone number).

> **Who can manage subscribers?**  
> Owners and Contributors can add, edit, and remove subscribers (on active events).

### Opening the Subscribers Tab

1. Open an event's detail page.
2. Click the **Subscribers** tab.

### Adding a Subscriber

1. Click **+ Add subscriber**.
2. Fill in the form:

   | Field | Required | Notes |
   |-------|----------|-------|
   | First name | Yes | |
   | Last name | Yes | |
   | Timezone | No | IANA timezone e.g. `America/New_York`. Defaults to UTC if omitted |
   | Channel | Yes | **Email** or **SMS** for the first contact |
   | Email address / Phone number | Yes | The contact address |
   | Label | No | Optional tag e.g. `work`, `personal` |
   | Set as primary | — | Checked by default for the first contact |

3. Click **Add subscriber**.

### Subscriber Statuses

| Status | Meaning |
|--------|---------|
| **Active** | Will receive reminders |
| **Unsubscribed** | Has opted out; will not receive reminders |

### Editing a Subscriber

Click **Edit** next to the subscriber's name to update their first name, last name, or timezone.

### Managing Contacts

Each subscriber can have multiple contacts (e.g. a work email and a personal email, or an email plus a phone number). Exactly one contact must be marked **Primary** at all times.

#### Adding a Contact

1. In the Subscribers tab, find the subscriber and click **+ Add contact**.
2. Choose a channel (**Email** or **SMS**).
3. Enter the contact value, an optional label, and tick **Set as primary contact** if applicable.
4. Click **Add contact**.

#### Editing a Contact

Click **Edit** next to a contact row to update its value, label, primary status, or active/inactive status.

#### Removing a Contact

Click **Remove** next to a contact and confirm. The contact must not be the only active contact of its type for that subscriber.

### Unsubscribing a Subscriber

Unsubscribing marks a subscriber as **Unsubscribed** so they stop receiving reminders without removing their record.

1. Click **Unsubscribe** next to the subscriber.
2. Confirm in the dialog.

To re-subscribe, edit the subscriber and change their status manually, or contact the event owner.

### Removing a Subscriber

Removing permanently deletes the subscriber and all their contacts from the event.

1. Click **Remove** next to the subscriber.
2. Confirm by clicking **Remove**.

> You cannot remove the last remaining active subscriber from an event. Unsubscribe them instead, or add another subscriber first.

---

---

## 5. Access Management

The **Access** tab lets the event owner share an event with other users and control what those users can do. The tab is only visible to the owner.

> **Owner only.** Contributors and Readers cannot see or use the Access tab.

### Roles

| Role | What they can do |
|------|------------------|
| **Owner** | Full control — edit event details, manage reminders, subscribers, and access grants. Only one owner per event. |
| **Contributor** | Can view and edit event content, manage reminders and subscribers. Cannot manage access grants. |
| **Reader** | Can view the event and its subscriber list, but cannot make any changes. |

The owner is always displayed and cannot be removed or demoted via this interface.

### Opening the Access Tab

1. Open an event's detail page.
2. Click the **Access** tab (only visible when you are the owner).

The tab shows a count of current grants and a list of every user who has been granted access.

### Granting Access to a User

1. Click **+ Grant access**.
2. Fill in the form:

   | Field | Required | Notes |
   |-------|----------|-------|
   | User ID | Yes | The UUID of the user you want to invite. This can be found on the user's profile page. |
   | Role | Yes | **Contributor** or **Reader** (default: Contributor) |

3. Click **Grant access**.

The user immediately appears in the grant list and gains access to the event in their own events view with a **Shared** badge.

#### Possible errors when granting access

| Error | Cause |
|-------|-------|
| *User ID is required* | The User ID field was left empty |
| *That user is already the owner of this event* | You entered your own user ID |
| *No active user found with that ID* | The ID does not match any registered, active account |
| *That user already has access. Edit their role instead.* | The user already has a grant on this event |

### Changing a User's Role

1. Click **Edit role** next to the user.
2. Select the new role (**Contributor** or **Reader**).
3. Click **Save changes**.

### Revoking Access

Revoking removes the user's access to the event entirely.

1. Click **Revoke** next to the user.
2. Review the confirmation dialog and click **Revoke access**.
3. To cancel without revoking, click **Keep**.

After revocation the event will no longer appear in the user's events list.

---

*More sections — Profile, API Keys and Email Branding — will be added in future editions of this manual.*

---

## 6. Reports

The **Reports** tab gives all event participants — owners, contributors, and readers — visibility into how each reminder was delivered.  Reports are generated automatically by the worker after every scheduled dispatch.

### Opening the Reports Tab

1. Open an event and click the **Reports** tab.
2. A list of all reminders for that event is displayed.
3. Click any reminder row to expand it and see its occurrence history.

### Understanding Occurrences

Each time a reminder fires it is recorded as one *occurrence*.  A one-off reminder will have a single occurrence; a recurring reminder accumulates one occurrence per run.  The occurrence count is shown next to each reminder in the list.

### Occurrence Report Columns

| Column | Description |
|--------|-------------|
| **Occ.** | Sequential occurrence number (1 = first dispatch). |
| **Date** | UTC timestamp when the report was recorded. |
| **Total** | Total number of dispatch jobs created (one per subscriber contact). |
| **Sent** | Dispatches that were delivered successfully. |
| **Failed** | Dispatches that could not be delivered after all retry attempts. |
| **Skipped** | Dispatches skipped (e.g. subscriber had no contact for the channel). |
| **Owner notified** | Whether a summary email was sent to the event owner, and when. |

### Viewing Failure Details

If an occurrence has one or more failed dispatches:

1. A **Show details** link appears in the rightmost column of that row.
2. Click **Show details** to expand an inline table listing each failure with its associated email address, channel, and failure reason.
3. Click **Hide details** to collapse the panel.

### Paginating Occurrences

Reminders with many occurrences are paginated at 20 rows per page.  Use the **← Previous** and **Next →** buttons below the table to navigate between pages.  The current page and total page count are shown between the buttons.

### What "Owner notified" Means

After each dispatch run the worker sends a brief delivery summary to the event owner.  The **Owner notified** column shows "Sent" together with the delivery timestamp when this notification was successfully sent.  "Not sent" indicates the notification is pending or was not triggered for that occurrence.

---

## 7. Admin Panel

The **Admin Panel** is accessible only to users with the *System Administrator* role.  It provides three management views: Users, Settings, and Events.

### Accessing the Admin Panel

Navigate to `/admin` in your browser.  If your account does not have the `SYSTEM_ADMIN` role you will be redirected to the Events page automatically.

### 7.1 Users Tab

The Users tab opens by default and lists every registered user in the system.

#### Searching for Users

Type a name or email fragment into the **Search** box and press **Search** to filter the list.  Clear the box and search again to see all users.

#### User Table Columns

| Column | Description |
|--------|-------------|
| **Name** | User's full name (first and last). |
| **Email** | Registered email address. |
| **Role** | `SYSTEM_ADMIN` (purple badge) or `USER` (grey badge). |
| **Status** | `ACTIVE` (green) or `DISABLED` (yellow). |
| **Actions** | Disable/Enable and Promote/Demote buttons (not shown for your own account). |

#### Disabling and Enabling Users

- Click **Disable** next to an active user to set their status to `DISABLED`.  Disabled users cannot log in.
- Click **Enable** next to a disabled user to restore their access.

You cannot disable or change the role of your own account through this panel.

#### Promoting and Demoting Administrators

- Click **Promote** to grant a regular user the `SYSTEM_ADMIN` role.
- Click **Demote** to remove the `SYSTEM_ADMIN` role and return the user to a regular `USER`.

### 7.2 Settings Tab

The Settings tab lists all system-wide configuration keys and their current values.

#### Editing a Setting

1. Click the **Edit** button in the row of the setting you want to change.
2. An inline text input appears pre-filled with the current value.
3. Edit the value and click **Save**.  A validation error is shown inline if the value is rejected (for example, `allow_public_registration` only accepts `true` or `false`).
4. Click **Cancel** to discard your changes and restore the original value.

#### Common Settings

| Key | Description |
|-----|-------------|
| `allow_public_registration` | `true` or `false` — whether the public `/register` page accepts new accounts. |
| `dispatch_poll_interval_seconds` | How often (in seconds, 10–3600) the worker polls for due reminders. |
| `dispatch_lookahead_seconds` | How far ahead (in seconds) the worker looks when querying upcoming reminders. |
| `dispatch_retry_max` | Maximum number of retry attempts for a failed dispatch. |
| `dispatch_retry_backoff_minutes` | Comma-separated back-off delays in minutes between retry attempts. |
| `event_archive_days` | Number of days after an event before it is automatically archived. |
| `default_email_wrapper_html` | Full HTML string used as the default email wrapper for event notifications. |

### 7.3 Events Tab

The Events tab shows every event across all users in reverse-creation order.

#### Events Table Columns

| Column | Description |
|--------|-------------|
| **Subject** | The event's subject line. |
| **Owner** | Full name of the user who owns the event (hover for their email address). |
| **Status** | `ACTIVE`, `CANCELLED`, or `ARCHIVED`. |
| **Date** | The scheduled event date (local-format). |
| **Created** | The date the event record was created. |

#### Pagination

When there are more than 20 events, **Previous** and **Next** navigation buttons appear below the table.  The **Previous** button is disabled on the first page.

---

*More sections — Profile, API Keys and Email Branding — will be added in future editions of this manual.*
