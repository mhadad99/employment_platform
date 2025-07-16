# Employment Platform: Requirements Analysis

## Functional Requirements

1. **User Registration and Authentication**
   - Users can register as either Employees or Employers.
   - Users can log in and log out securely.

2. **Employee Profile Management**
   - Employees can create and edit their profiles, including bio, city, experience level, and programming languages.
   - Employees can add or remove programming languages from their profiles.

3. **Employer Profile Management**
   - Employers can create and edit their profiles, including company information.

4. **Job Posting and Management**
   - Employers can create, update, and delete job postings.
   - Jobs include title, description, and required programming languages.

5. **Job Search and Application**
   - Employees can view and search for jobs.
   - Employees can apply for jobs.
   - Duplicate applications are prevented.

6. **Notifications**
   - Employees receive notifications when a new job matches their skills or bio.
   - Employers receive notifications when an employee applies for their job.
   - Employees receive notifications when their application status changes.
   - Employees are notified when someone views their profile.

7. **Profile Views**
   - Profile views are tracked, and employees can see how many times their profile has been viewed.

8. **Admin Management**
   - Admins can manage users, jobs, and other platform data via the Django admin interface.

## Non-Functional Requirements

1. **Usability**
   - The platform provides a user-friendly web interface for all user actions.
   - Forms include validation and helpful error messages.

2. **Performance**
   - The system should handle multiple users and job postings efficiently.
   - Notifications and queries are optimized to avoid unnecessary database load.

3. **Security**
   - User data is protected using Django's authentication and permission system.
   - Sensitive actions (like posting jobs or editing profiles) require authentication.
   - Passwords are securely hashed.

4. **Scalability**
   - The platform is designed to support growth in the number of users and jobs.
   - Uses PostgreSQL for robust data management.

5. **Maintainability**
   - The codebase follows Django best practices and is organized by app (users, jobs).
   - Signals are used for decoupled notification logic.

6. **Reliability**
   - The system should handle errors gracefully and provide meaningful feedback to users.
   - Automated tests can be added to ensure core functionality.

7. **Extensibility**
   - The platform can be extended with new features, such as messaging or advanced search.

8. **Localization**
   - The system uses English by default but can be extended for other languages.

## Use Cases

### Use Case 1: User Registration

**Actors:** Employee, Employer  
**Description:**  
A user registers as either an employee or employer by providing required information.  
**Main Flow:**  
1. User selects registration type (employee/employer).
2. User fills out registration form.
3. System creates a new user account and profile.
4. User receives confirmation and can log in.

---

### Use Case 2: Employee Profile Management

**Actor:** Employee  
**Description:**  
An employee manages their profile, including bio, skills, and experience.  
**Main Flow:**  
1. Employee logs in.
2. Employee navigates to profile page.
3. Employee edits bio, city, experience, and programming languages.
4. System saves changes and updates the profile.

---

### Use Case 3: Employer Profile Management

**Actor:** Employer  
**Description:**  
An employer manages their company profile.  
**Main Flow:**  
1. Employer logs in.
2. Employer navigates to profile page.
3. Employer edits company information.
4. System saves changes.

---

### Use Case 4: Job Posting

**Actor:** Employer  
**Description:**  
An employer posts a new job.  
**Main Flow:**  
1. Employer logs in.
2. Employer navigates to job posting page.
3. Employer fills out job details (title, description, required skills).
4. System creates the job post.
5. System automatically notifies employees whose skills or bio match the job.

---

### Use Case 5: Job Search and Application

**Actor:** Employee  
**Description:**  
An employee searches for jobs and applies to suitable ones.  
**Main Flow:**  
1. Employee logs in.
2. Employee searches or browses job listings.
3. Employee views job details.
4. Employee applies for a job.
5. System records the application and notifies the employer.

---

### Use Case 6: Notification of Matching Jobs

**Actor:** Employee  
**Description:**  
Employees are notified when a new job matches their skills or bio.  
**Main Flow:**  
1. Employer posts a new job.
2. System finds employees whose skills or bio match the job.
3. System sends notifications to those employees.

---

### Use Case 7: Employer Notification of Applications

**Actor:** Employer  
**Description:**  
Employers are notified when an employee applies for their job.  
**Main Flow:**  
1. Employee applies for a job.
2. System sends a notification to the employer.

---

### Use Case 8: Profile View Tracking

**Actor:** Employee  
**Description:**  
Employees can see how many times their profile has been viewed.  
**Main Flow:**  
1. Another user views an employee's profile.
2. System increments the profile view count.
3. Employee can view the count on their profile page.

---

### Use Case 9: Admin Management

**Actor:** Admin  
**Description:**  
Admins manage users, jobs, and platform data.  
**Main Flow:**  
1. Admin logs into the admin interface.
2. Admin views, edits, or deletes users and jobs as needed.

---

## Logical Design (ERD) for Employment Platform

Below is a textual Entity-Relationship Diagram (ERD) representing the main entities and their relationships:

---

## Entities and Relationships

- **User**
  - (Django built-in, referenced by Employee, Employer, Profile, ProfileView)

- **Employer**
  - user (OneToOne → User)
  - name, email, username, image_avatar, company, city, created, id

- **Employee**
  - user (OneToOne → User)
  - national_id, name, email, username, image_avatar, city, bio, experience_level, created, id
  - programming_languages (ManyToMany → ProgrammingLanguage)

- **ProgrammingLanguage**
  - language, created, id

- **Job**
  - title, description, created_at, updated_at
  - programming_languages (ManyToMany → ProgrammingLanguage)
  - employer (ForeignKey → Employer)
  - employee (ForeignKey → Employee, nullable)

- **JobApplication**
  - job (ForeignKey → Job)
  - employee (ForeignKey → Employee)
  - status, applied_at

- **Notification**
  - recipient (ForeignKey → Employee)
  - message, is_read, created_at

- **ProfileView**
  - employee (ForeignKey → Employee)
  - viewer (ForeignKey → User)
  - timestamp, id

- **Profile**
  - user (OneToOne → User)
  - user_type

---

## Relationships

- **User** 1---1 **Employee**
- **User** 1---1 **Employer**
- **User** 1---1 **Profile**
- **Employee** M---M **ProgrammingLanguage**
- **Job** M---M **ProgrammingLanguage**
- **Employer** 1---M **Job**
- **Employee** 1---M **JobApplication**
- **Job** 1---M **JobApplication**
- **Employee** 1---M **Notification**
- **Employee** 1---M **ProfileView**
- **User** 1---M **ProfileView** (as viewer)

---

## ERD Diagram (Textual)

```
User
 ├── 1:1 ──> Employee
 ├── 1:1 ──> Employer
 └── 1:1 ──> Profile

Employee
 ├── M:M ──> ProgrammingLanguage
 ├── 1:M ──> JobApplication
 ├── 1:M ──> Notification
 └── 1:M ──> ProfileView

Employer
 └── 1:M ──> Job

Job
 ├── M:M ──> ProgrammingLanguage
 ├── 1:M ──> JobApplication
 └── 0..1:1 ──> Employee (optional, for assignment)

JobApplication
 ├── M:1 ──> Job
 └── M:1 ──> Employee

Notification
 └── M:1 ──> Employee

ProfileView
 ├── M:1 ──> Employee
 └── M:1 ──> User (viewer)

Profile
 └── 1:1 ──> User
```

---

**Note:**  
- All relationships are based on your Django models.
- You can visualize this diagram using tools like dbdiagram.io, Lucidchart, or draw.io for a graphical ERD.

---

## Summary

This employment platform enables employers to post jobs and employees to find and apply for jobs matching their skills. The system provides real-time notifications, profile management, and secure authentication, all built on a scalable and maintainable Django architecture.