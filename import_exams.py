#!/usr/bin/env python3
"""Import exam data from pasted text to Supabase schedule table"""

import json
import re
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = 'https://fgewwriulwdodmlbsotp.supabase.co'
SUPABASE_KEY = 'sb_publishable_yvdyY62yUu7HgPw7wjy9XQ_jmcje9te'

def parse_exam_file(filepath):
    """Parse the pasted text file and extract exam data"""
    exams = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Skip header line
    for line in lines[1:]:
        parts = line.strip().split('\t')
        if len(parts) < 7:
            continue
        
        code = parts[0].strip()
        component = parts[1].strip()
        long_name = parts[2].strip()
        start_dt = parts[3].strip()  # "YYYY/MM/DD HH:MM"
        end_dt = parts[4].strip()
        # parts[5] = duration number
        room = parts[6].strip() if len(parts) > 6 else ''
        
        if not start_dt or not room:
            continue
        
        # Parse datetime
        dt_match = re.match(r'(\d{4}/\d{2}/\d{2})\s+(\d{2}:\d{2})', start_dt)
        if not dt_match:
            continue
        
        date = dt_match.group(1)  # YYYY/MM/DD
        start_time = dt_match.group(2)  # HH:MM
        
        # Parse end time
        end_match = re.match(r'(\d{4}/\d{2}/\d{2})\s+(\d{2}:\d{2})', end_dt)
        if end_match:
            end_time = end_match.group(2)
        else:
            end_time = start_time
        
        # Use component as class_name, or long_name
        class_name = component if component else long_name
        
        exams.append({
            'date': date,
            'start_time': start_time,
            'end_time': end_time,
            'class_name': class_name,
            'room': room
        })
    
    return exams

def clear_schedule_table(client):
    """Clear existing records from schedule table"""
    try:
        # Use direct SQL or delete all records
        response = client.table('schedule').delete().neq('id', 0).execute()
        print(f"Cleared schedule table: {len(response.data) if response.data else 0} records deleted")
        return True
    except Exception as e:
        print(f"Error clearing schedule table: {e}")
        return False

def import_exams(client, exams):
    """Import exams to schedule table"""
    # First, clear existing records
    clear_schedule_table(client)
    
    # Import each exam
    success_count = 0
    for exam in exams:
        try:
            response = client.table('schedule').insert({
                'date': exam['date'],
                'start_time': exam['start_time'],
                'end_time': exam['end_time'],
                'class_name': exam['class_name'],
                'room': exam['room'],
                'teacher': 'EXAM'  # Mark as exam, not protection
            }).execute()
            
            if response.data:
                success_count += 1
        except Exception as e:
            print(f"Error inserting exam: {e}")
            continue
    
    return success_count

def main():
    # Initialize Supabase client
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Parse exam file
    exam_file = '/Users/christina.feng/.minimax-agent-cn/projects/pasted-text-2026-05-08T08-47-20.txt'
    exams = parse_exam_file(exam_file)
    
    print(f"Parsed {len(exams)} exams from file")
    
    # Filter only B-room exams (not Boarding rooms)
    b_room_exams = [e for e in exams if e['room'].startswith('B')]
    print(f"B-room exams: {len(b_room_exams)}")
    
    # Show sample
    print("\nSample exams:")
    for exam in b_room_exams[:5]:
        print(f"  {exam['date']} {exam['start_time']}-{exam['end_time']} | {exam['room']} | {exam['class_name']}")
    
    # Import
    count = import_exams(client, b_room_exams)
    print(f"\nImported {count} exams to schedule table")

if __name__ == '__main__':
    main()