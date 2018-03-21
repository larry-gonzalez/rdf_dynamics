x = [20170418, 20170425, 20170503, 20170509, 20170516, 20170524, 20170530, 20170607, 20170613, 20170620, 20170627, 20170712, 20170718, 20170725]
y = [1292765, 1304617, 1317837, 1321923, 1326763, 1333415, 1339292, 1344527, 1348416, 1354409, 1361410, 1381581, 1415836, 1435990]

mx = sum(x)/len(x)
my = sum(y)/len(y)

x_mx = [_ - mx for _ in x]
y_my = [_ - my for _ in y]

num = sum([x_mx[i]*y_my[i] for i in range(len(x_mx))])
den = sum([x_mx[i]*x_mx[i] for i in range(len(x_mx))])

m = float(num)/den
b = my- m*mx

p = [int(round(m*_+b)) for _ in x]

e2 = [(p[i]-y[i])*(p[i]-y[i]) for i in range(len(x))]
