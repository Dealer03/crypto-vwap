import pandas as pd
from datetime import datetime
from ..models import Transaction  # Import your Transaction model


def import_transactions_from_csv(csv_file_path, user):
    try:
        # Read the CSV file using pandas
        df = pd.read_csv(csv_file_path, encoding='ANSI')

        # Iterate over rows and save transactions
        for index, row in df.iterrows():
            # Strip leading and trailing whitespace
            time_str = row['Time'].strip()

            # Check if the datetime string is empty
            if not time_str:
                continue

            # Convert date string to datetime object
            time = datetime.strptime(time_str, '%Y-%m-%d%H:%M:%S')

            # Create or update Transaction object
            transaction = Transaction.objects.create(
                user=user,
                date=time.date(),
                side=row['Side'],
                sub_wallet=row['Sub-wallet'],
                type=row['Type'],
                asset=row['Asset'],
                average=float(row['Average']),
                filled=float(row['Filled']),
                fees=float(row['Fees']),
                realized_profit=float(row['Realized Profit']),
            )

        return True, None  # Return success and no error message
    except Exception as e:
        return False, str(e)  # Return failure and error message
