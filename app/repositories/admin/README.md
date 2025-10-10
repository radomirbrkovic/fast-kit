# Repositories

This folder contains the **data access layer** of the application.  
Repositories are responsible for communicating with the database, executing queries, and returning results to the services.

## Structure
- **CrudRepository** – provides common CRUD operations (create, read, update, delete).  
- **UserRepository** – handles user-specific queries (find by email, role, etc.).  
- **PageRepository** – handles page-specific queries for public pages.  
- *(add more repositories as needed, each focusing on one entity/domain).*

## Guidelines
- Each repository should extend `CrudRepository` whenever possible.  
- Keep repository methods focused on **database operations only** (no business logic here).  
- Return clean models/DTOs to the services layer.  
- If a query is too complex, consider adding comments or splitting it into smaller reusable methods.
