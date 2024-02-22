import os


def rm_files(year, service):
    for i in range(12):
        
        # sets the month part of the file_name string
        month = '0'+str(i+1)
        month = month[-2:]

        # csv file_name
        file_name_csv = f"{service}_tripdata_{year}-{month}.csv.gz"
        file_name_parquet = f"{service}_tripdata_{year}-{month}.parquet"

        os.remove(f'C:/Users/Utilizador/Documents/dataengineer-zoomcamp2024/{file_name_csv}')
        os.remove(f'C:/Users/Utilizador/Documents/dataengineer-zoomcamp2024/{file_name_parquet}')





#rm_files('2019', 'green')
#rm_files('2020', 'green')
#rm_files('2020', 'yellow')
#rm_files('2019', 'yellow')
rm_files('2019', 'fhv')