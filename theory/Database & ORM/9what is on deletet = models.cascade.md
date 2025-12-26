8. What is on_delete = models.CASCADE?
Simple Explanation
•If parent is deleted
•child data is also deleted
Example:
    Delete Category -> Delete all its Posts


9. What is Django Migration?
Problem Without Migration
    •Django doesn't know when model changes
    •Database becomes outdated
        
    Solution: Migration
            Migration is Django's way of tracking and applying database changes




    Migration Flow
    
    models.py->migration file->migrate->database tables


1O. Why Two Migration Commands?
•Checks what changed
•Creates instructions
migrate
•Applies changes to database
•Creates/updates tables




11. What is Django ORM Querying?
Simple Meaning
Querying means asking questions to the database
Examples:
•Give me all posts
•Give me one post
•Delete a post


Python(Django) | Database
Class | Table
Attribute | Column
Object | Row
Python Code | SQL Query