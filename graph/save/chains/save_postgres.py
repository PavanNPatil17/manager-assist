
from dotenv import load_dotenv
load_dotenv()
import sys
from pathlib import Path

# Add project root to path to run directly the file
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
import psycopg2
from psycopg2.extras import Json
import os

from graph.save.save_graph_state import NormalizedMemory



def save_to_postgres(normalized_memory: NormalizedMemory, user_id: str, org_id: str) -> str:
    """
    Save NormalizedMemory to PostgreSQL cortex.manager_memory table.
    
    Args:
        normalized_memory: The normalized memory object to save
        user_id: User ID from the context
        org_id: Organization ID from the context
        
    Returns:
        str: The UUID of the inserted record
    """
    # Get database connection details from environment
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "mydb"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )
    
    try:
        cursor = conn.cursor()
        
        # Insert into manager_memory table
        insert_query = """
            INSERT INTO cortex.manager_memory (
                org_id, user_id, category, subcategory, title, summary,
                facts, entities, memory_date, confidence, source, created_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING id;
        """
        
        cursor.execute(insert_query, (
            org_id,
            user_id,
            normalized_memory.category,  # PostgreSQL array
            normalized_memory.subcategory,
            normalized_memory.title,
            normalized_memory.summary,
            Json(normalized_memory.facts),  # JSONB
            Json(normalized_memory.entities),  # JSONB
            normalized_memory.memory_date,
            normalized_memory.confidence,
            normalized_memory.source,
            normalized_memory.created_at
        ))
        
        memory_id = cursor.fetchone()[0]
        conn.commit()
        
        print(f"Successfully saved memory to PostgreSQL with ID: {memory_id}")
        
        return str(memory_id)
        
    except Exception as e:
        conn.rollback()
        print(f"Error saving to PostgreSQL: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def get_memory_by_id(memory_id: str) -> dict:
    """
    Retrieve a memory record from PostgreSQL cortex.manager_memory table by ID.

    Args:
        memory_id: The UUID of the memory record to retrieve

    Returns:
        dict: The memory record as a dictionary, or None if not found
    """
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "mydb"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )

    try:
        cursor = conn.cursor()
        select_query = """
            SELECT id, org_id, user_id, category, subcategory, title, summary,
                    facts, entities, memory_date, confidence, source, created_at
            FROM cortex.manager_memory
            WHERE id = %s;
        """
        cursor.execute(select_query, (memory_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))
    except Exception as e:
        print(f"Error retrieving memory from PostgreSQL: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    result = get_memory_by_id("621c264a-abf3-4fc5-9ece-1f360891694d")  # Replace with actual UUID for testing
    print(result)