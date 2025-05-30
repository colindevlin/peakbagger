# seed_db.py
from models import Peak, PeakList, db_session

# Create some peak lists
rmnp_list = PeakList(name="RMNP")
cofourteeners = PeakList(name="Colorado 14ers")
cothirteeners = PeakList(name="Colorado 13ers")

# Create some peaks
longs = Peak(name="Longs Peak", range="Front Range")
meeker = Peak(name="Mount Meeker", range="Front Range")
elbert = Peak(name="Mount Elbert", range="Sawatch Range")

# Add peaks to lists
rmnp_list.peaks.extend([longs, meeker])
cofourteeners.peaks.extend([longs, elbert])
cothirteeners.peaks.append(meeker)

# Add everything to session and commit
db_session.add_all([rmnp_list, cofourteeners, cothirteeners])
db_session.commit()

print("Database seeded successfully.")
