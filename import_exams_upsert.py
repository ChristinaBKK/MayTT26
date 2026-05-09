#!/usr/bin/env python3
"""Import exam data from pasted text to Supabase schedule table with upsert logic"""

import json
import re

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

def get_existing_exams(client):
    """Get all existing exams from schedule table"""
    response = client.table('schedule').select('id, date, start_time, end_time, class_name, room').execute()
    return {f"{s['date']}|{s['start_time']}|{s['room']}": s for s in response.data}

def upsert_exams(client, exams):
    """Import exams with upsert logic - update if exists, insert if new"""
    # Get existing exams
    existing = get_existing_exams(client)
    print(f"Found {len(existing)} existing records in schedule table")
    
    # Track changes
    updated = 0
    inserted = 0
    skipped = 0
    
    for exam in exams:
        key = f"{exam['date']}|{exam['start_time']}|{exam['room']}"
        
        if key in existing:
            # Update existing record
            existing_id = existing[key]['id']
            try:
                response = client.table('schedule').update({
                    'end_time': exam['end_time'],
                    'class_name': exam['class_name']
                }).eq('id', existing_id).execute()
                updated += 1
                print(f"  Updated: {exam['date']} {exam['room']} - {exam['class_name'][:30]}...")
            except Exception as e:
                print(f"  Error updating: {e}")
                skipped += 1
        else:
            # Insert new record
            try:
                response = client.table('schedule').insert({
                    'date': exam['date'],
                    'start_time': exam['start_time'],
                    'end_time': exam['end_time'],
                    'class_name': exam['class_name'],
                    'room': exam['room'],
                    'teacher': 'EXAM'
                }).execute()
                inserted += 1
                print(f"  Inserted: {exam['date']} {exam['room']} - {exam['class_name'][:30]}...")
            except Exception as e:
                print(f"  Error inserting: {e}")
                skipped += 1
    
    return {'updated': updated, 'inserted': inserted, 'skipped': skipped}

def main():
    from supabase import create_client
    
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
    print("\nSample exams to import:")
    for exam in b_room_exams[:5]:
        print(f"  {exam['date']} {exam['start_time']}-{exam['end_time']} | {exam['room']} | {exam['class_name'][:40]}")
    
    # Upsert
    print("\n" + "="*50)
    result = upsert_exams(client, b_room_exams)
    print("="*50)
    print(f"Result: {result['inserted']} inserted, {result['updated']} updated, {result['skipped']} skipped")

if __name__ == '__main__':
    main()