#!/usr/bin/env python3
"""Import exam data with Code - Title format"""

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
        # parts[6] = duration string
        room = parts[7].strip() if len(parts) > 7 else ''  # Room is in column 8 (index 7)
        
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
        
        # Clean room name - remove trailing spaces
        room = room.strip()
        
        # Format: Code - Component
        if code and component:
            class_name = f"{code} - {component}"
        elif code:
            class_name = code
        else:
            class_name = long_name
        
        # Only include B-room exams (exact match for B followed by digits)
        if not re.match(r'^B\d+$', room):
            continue
        
        exams.append({
            'date': date,
            'start_time': start_time,
            'end_time': end_time,
            'class_name': class_name,
            'room': room
        })
    
    return exams

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
    print("\nSample B-room exams:")
    for exam in b_room_exams[:5]:
        print(f"  {exam['date']} {exam['room']} | {exam['class_name']}")
    
    # Insert exams
    inserted = 0
    print("\nImporting...")
    for exam in b_room_exams:
        try:
            response = client.table('schedule').insert({
                'date': exam['date'],
                'start_time': exam['start_time'],
                'end_time': exam['end_time'],
                'class_name': exam['class_name'],
                'room': exam['room'],
                'teacher': 'EXAM'
            }).execute()
            if response.data:
                inserted += 1
                if inserted <= 10:
                    print(f"  ✓ {exam['date']} {exam['room']} | {exam['class_name']}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            continue
    
    print(f"\n✓ Total inserted: {inserted} exams")

if __name__ == '__main__':
    main()