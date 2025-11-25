try:
    import datablockAPI
    print("Import successful")
except Exception as e:
    print(f"Error importing: {e}")
    import traceback
    traceback.print_exc()
