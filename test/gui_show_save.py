import uplt
import imageio.v3 as iio # type: ignore

## Run Mode

save_to_file = False
engine = 'mpl'

## Data

x = [4, 5, 6, 8]

y1 = [1, 2, 3, 4]
y2 = [4, 3, 2, 1]

## Fig 1

f1 = uplt.figure(engine=engine)
f1.plot(x, y1)
f1.plot(x, y2, line_style=':', color='gray')
f1.scatter(3, 5, name='The lonely dot')
f1.title('Test')
f1.legend(True)
f1.axis_aspect('equal')
f1.xlabel('X value')
f1.ylabel('Y value')

if save_to_file:
    f1.save('fig1.save.jpg')
    iio.imwrite('fig1.as_image.png', f1.as_image())
else:
    f1.show(block=False)

## Fig 2

f2 = uplt.figure(engine=engine, aspect_ratio=0.4)
f2.plot(y1, x, name='#1', line_style='--')
f2.plot(y2, x)
f2.title('Test')
f2.legend(True)
f2.xlabel('X value')
f2.ylabel('Y value')
f2.xlim(-0.5)
f2.ylim(0)

if save_to_file:
    f2.save('fig2.save.jpg')
    iio.imwrite('fig2.as_image.png', f2.as_image())
else:
    f2.show()
