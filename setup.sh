cd virt/lib/python3.6/site-packages/
zip -r9 ../../../../function.zip .
cd ../../../../
zip -g function.zip *.py
python setup_lambda.py