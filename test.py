o=open("../bank_system/data", "r")
data=o.readlines()
o.close()

for d in data:
    print(d)
print(data)
balance=data[3].split(",")[-1].strip() # تحويل إلى ليست ثم اختيار آخر عنصر ثم حذف باكسلاش إن ثم الحصول على الرصيد

balance=int(balance)+10

data[3]=data[3].split(",")[:-1] # تحويل إلى ليست مع حذف آخر عنصر

data[3].append(str(balance)+"\n")
data[3]=",".join(data[3]) # تحويل إلى سترنج
o=open("../bank_system/data", "w") # فتح الملف فى وضع الكتابة

 # كتابة المحتويات الجديدة مع حذف القديمة
