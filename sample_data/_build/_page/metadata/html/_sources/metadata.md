---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

```{code-cell} ipython3
import pandas as pd

```

```{code-cell} ipython3
data = pd.read_csv('sample_3m.csv')
```

```{code-cell} ipython3
data.info()
```

## Property Information

**property_id**: The idendification number for each regested property. (Mock)

**property_capacity**: What kind of group this property can hold. (Mock)

**property_address**: Real world postcode and its corresponding state and name.

## Order Information

**booking_id**: Non-unique booking id, this can be made unique or non-unique for test purpose.

**check_in_date**: Date between 01/01/23 - 30/06/23.

**check_out_date**: Date after check_in_date with 1-15 days more.

**base_fee**: Random number.

**service_fee**: 15% based on base_fee.

**cleaning_fee**: Random proportion based on base_fee.

**gst**: 10% based on base+service+cleaning_fee. 

**total_price**: gst * 110%.

## Owner Information

**owner_id**: Non-unique booking id, this can be made unique or non-unique for test purpose, 4-5 digits.

**abn**: 11 digits number in ABN's format, 80% chance of having this.

**tin**: 9 digits number if ABN is missing.

**dob**: Random date between 01/01/1940 - 31/12/1999.

**contact_number**: All contact_numbers are in Aussie style (+614*********).

**email**: first_name.last_name@gmail.com.

**rating**: Integer between 0 - 10.

### 80% chance inside Australia
* **owner_location**: Australia in this case.
* **owner_address**: Real world postcode and its corresponding state and name.
* **bank_account_name**: Fake name.
* **bsb**: 062***.
* **bank_account_number**: 1*** ****.
* **bank_name**: Commonwealth Bank of Australia in this case.
* **paypal_id**: 45% chance of having first_name.last_name@paypal.com, 45% having contact_number@paypal.com, 10% having empty.

### 20% chance in New Zealand
* **owner_location**: New Zealand in this case.
* **owner_address**: Auckland, NZ in this case.
* **bank_name**: ANZ Bank in this case.
* **iban**: AU********.
* **swift_code**: CTBAAU2S in this case.
  
## Order Status

**order_status**: 80% Completed, 8% Cancelled, 8% Refunded, 4% Parcially Refunded.

**final_price**: Completed: 100% totoal_price, Cancelled/Refunded: 0% totoal_price, Parcially Refunded: 50%-90% total_price.

**final_gst**: final_price / 11.