import sys, os
sys.path.insert(0, os.getcwd())
modules = ['models.db','services.allocation_service','services.room_service','services.student_service','routes']
for m in modules:
    try:
        __import__(m)
        print('OK_IMPORT', m)
    except Exception as e:
        print('ERR_IMPORT', m, type(e).__name__, e)
print('DONE')
