# Control Points File Format

## Curve

The text file should include a list of _(x, y)_ coordinates. For instance, `CP_Curve1.txt` file contains the following control points:

* 05,10
* 15,25
* 30,30
* 45,05
* 55,05
* 70,40
* 60,60
* 35,60
* 20,40

Therefore, the format of the control points file is;

| X  | Y  |
| :---: | :---: |
| 05 | 10 |
| 15 | 25 |
| 30 | 30 |
| 45 | 05 |
| 55 | 05 |
| 70 | 40 |
| 60 | 60 |
| 35 | 60 |
| 20 | 40 |

The method to read control points from a file structured like the above is

* `read_ctrlpts(file_name)`

## Surface

The text file should include _(x, y, z)_ coordinates. The structure of the text file includes two directions, namely **u** and **v**.

Therefore, the format of the control points file is;

| | u0 | u1 | u2 | u3 | u4 | u5 | u6 | u7 | u8 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **v0** | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ |
| **v1** | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ |
| **v2** | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ |
| **v3** | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ |
| **v4** | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ |
| **v5** | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ |
| **v6** | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ |
| **v7** | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ |
| **v8** | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ | _(x, y, z)_ |

This structure corresponds to a right-handed coordinate system.

The methods to read control points from a file structured like the above are

* `read_ctrlpts(file_name)` for files containing _(x, y, z)_ style control points.
* `read_ctrlptsw(file_name)` for files containing _(x\*w, y\*w, z\*w, w)_ style weighted control points.
