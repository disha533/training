from database import get_connection
def add_student(student):
    conn=get_connection()
    cursor=conn.cursor()
    query= """
    INSERT INTO student(id,name,age,email,branch,year)
    VALUES(:1,:2,:3,:4)
    """
    cursor.execute(query,(
        student.id,
        student.name,
        student.age,
        student.branch,
        student.year
        
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message":"student added"}

    
    