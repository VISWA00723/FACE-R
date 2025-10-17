"""
Database Migration: Single Embedding to Multiple Embeddings

This script migrates the database from storing a single averaged embedding
to storing multiple individual embeddings per employee.

IMPORTANT: Run this before starting the updated backend!
"""
import psycopg2
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded .env from {env_path}")
else:
    print(f"⚠️  .env not found at {env_path}, using environment variables")

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/face_recognition_db')


def migrate_database():
    """Migrate from embedding_vector to embedding_vectors"""
    
    print("=" * 60)
    print("Database Migration: Single to Multiple Embeddings")
    print("=" * 60)
    
    try:
        # Connect to database
        print(f"\n1. Connecting to database...")
        print(f"   URL: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}")
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        print("✅ Connected successfully")
        
        # Check if migration is needed
        print("\n2. Checking if migration is needed...")
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'employees' AND column_name IN ('embedding_vector', 'embedding_vectors')
        """)
        columns = [row[0] for row in cur.fetchall()]
        
        if 'embedding_vectors' in columns and 'embedding_vector' not in columns:
            print("✅ Migration already completed!")
            return
        
        if 'embedding_vector' not in columns:
            print("❌ Error: embedding_vector column not found!")
            return
        
        print("⚠️  Migration needed")
        
        # Get employee count
        cur.execute("SELECT COUNT(*) FROM employees")
        emp_count = cur.fetchone()[0]
        print(f"\n3. Found {emp_count} employees to migrate")
        
        if emp_count == 0:
            print("⚠️  No employees found. Skipping data migration.")
        else:
            # Fetch all employees
            print("\n4. Fetching employee data...")
            cur.execute("SELECT id, employee_id, embedding_vector FROM employees")
            employees = cur.fetchall()
            print(f"✅ Fetched {len(employees)} employee records")
        
        # Add new column
        print("\n5. Adding embedding_vectors column...")
        cur.execute("""
            ALTER TABLE employees 
            ADD COLUMN IF NOT EXISTS embedding_vectors JSON
        """)
        print("✅ Column added")
        
        # Migrate data
        if emp_count > 0:
            print("\n6. Migrating embedding data...")
            for idx, (emp_id, employee_id, embedding_vector) in enumerate(employees, 1):
                # Convert single embedding to list of embeddings
                # Wrap the single embedding in an array
                embedding_vectors = [embedding_vector]
                
                cur.execute("""
                    UPDATE employees 
                    SET embedding_vectors = %s 
                    WHERE id = %s
                """, (json.dumps(embedding_vectors), emp_id))
                
                print(f"   Migrated {idx}/{len(employees)}: {employee_id}")
            
            print("✅ All embeddings migrated")
        
        # Make new column NOT NULL (after migration)
        print("\n7. Setting embedding_vectors as NOT NULL...")
        cur.execute("""
            ALTER TABLE employees 
            ALTER COLUMN embedding_vectors SET NOT NULL
        """)
        print("✅ Constraint added")
        
        # Drop old column
        print("\n8. Dropping old embedding_vector column...")
        cur.execute("""
            ALTER TABLE employees 
            DROP COLUMN IF EXISTS embedding_vector
        """)
        print("✅ Old column dropped")
        
        # Commit changes
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Start the backend server")
        print("2. Existing employees will work with their single embedding")
        print("3. New registrations will store multiple embeddings")
        print("4. Re-register employees gradually for best accuracy")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        if conn:
            conn.rollback()
        raise
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        print("\n✅ Database connection closed")


def rollback_migration():
    """Rollback: Multiple embeddings back to single embedding"""
    
    print("=" * 60)
    print("ROLLBACK: Multiple to Single Embedding")
    print("=" * 60)
    
    try:
        # Connect to database
        print(f"\n1. Connecting to database...")
        print(f"   URL: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}")
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        print("✅ Connected successfully")
        
        # Check current state
        print("\n2. Checking current state...")
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'employees' AND column_name IN ('embedding_vector', 'embedding_vectors')
        """)
        columns = [row[0] for row in cur.fetchall()]
        
        if 'embedding_vector' in columns and 'embedding_vectors' not in columns:
            print("✅ Already using single embedding!")
            return
        
        if 'embedding_vectors' not in columns:
            print("❌ Error: embedding_vectors column not found!")
            return
        
        # Get employee count
        cur.execute("SELECT COUNT(*) FROM employees")
        emp_count = cur.fetchone()[0]
        print(f"\n3. Found {emp_count} employees")
        
        # Add old column back
        print("\n4. Adding embedding_vector column...")
        cur.execute("""
            ALTER TABLE employees 
            ADD COLUMN IF NOT EXISTS embedding_vector JSON
        """)
        print("✅ Column added")
        
        if emp_count > 0:
            # Migrate data back (average multiple embeddings)
            print("\n5. Rolling back embedding data (averaging)...")
            cur.execute("SELECT id, employee_id, embedding_vectors FROM employees")
            employees = cur.fetchall()
            
            for idx, (emp_id, employee_id, embedding_vectors) in enumerate(employees, 1):
                # Average all embeddings
                import numpy as np
                embeddings = np.array(embedding_vectors, dtype=np.float32)
                avg_embedding = np.mean(embeddings, axis=0)
                avg_embedding = avg_embedding / np.linalg.norm(avg_embedding)
                
                cur.execute("""
                    UPDATE employees 
                    SET embedding_vector = %s 
                    WHERE id = %s
                """, (json.dumps(avg_embedding.tolist()), emp_id))
                
                print(f"   Rolled back {idx}/{len(employees)}: {employee_id}")
            
            print("✅ All embeddings rolled back")
        
        # Make old column NOT NULL
        print("\n6. Setting embedding_vector as NOT NULL...")
        cur.execute("""
            ALTER TABLE employees 
            ALTER COLUMN embedding_vector SET NOT NULL
        """)
        print("✅ Constraint added")
        
        # Drop new column
        print("\n7. Dropping embedding_vectors column...")
        cur.execute("""
            ALTER TABLE employees 
            DROP COLUMN IF EXISTS embedding_vectors
        """)
        print("✅ New column dropped")
        
        # Commit changes
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✅ ROLLBACK COMPLETED!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        if conn:
            conn.rollback()
        raise
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        print("\n✅ Database connection closed")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate database embeddings")
    parser.add_argument('--rollback', action='store_true', help='Rollback to single embedding')
    args = parser.parse_args()
    
    if args.rollback:
        confirm = input("\n⚠️  Are you sure you want to ROLLBACK? (yes/no): ")
        if confirm.lower() == 'yes':
            rollback_migration()
        else:
            print("Rollback cancelled")
    else:
        confirm = input("\n⚠️  This will modify your database. Continue? (yes/no): ")
        if confirm.lower() == 'yes':
            migrate_database()
        else:
            print("Migration cancelled")
