# brexero
Export from Brex, import to Xero.

This allows you to add your Brex card account as a Bank account in Xero.

1. Create a new bank account in Xero, with the type "credit card".
2. Go into the Brex web interface, choose the date range, and export as csv.
3. Run brexero.py, as such:

```
python brexero.py --brex-file <exported file from step 2> --xero-file <file to write to>`
```

4. In the Brex account in Xero, import the CSV generate above.

