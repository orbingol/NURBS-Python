# Control Points File Format

## Curves

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

| x  | y  |
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

In order to generate the weighted control points file structure, you should multiply x and y values by the weight, _"w"_. An example file, `CPw_Curve4.txt`, is shown below:

| x\*w | y\*w | w |
| :---: | :---: | :---: |
| 0 | -1 | 1 |
| -0.707 | -0.707 | 0.707 |
| -1 | 0 | 1 |
| -0.707 | 0.707 | 0.707 |
| 0 | 1 | 1 |
| 0.707 | 0.707 | 0.707 |
| 1 | 0 | 1 |
| 0.707 | -0.707 | 0.707 |
| 0 | -1 | 1| 

The unweighted version of `CPw_Curve4.txt` file is;

| x  | y  |
| :---: | :---: |
| 0 | -1 |
| -1 | -1 |
| -1 | 0 |
| -1 | 1 |
| 0 | 1 |
| 1 | 1 |
| 1 | 0 |
| 1 | -1 |
| 0 | -1 |

The method to read control points from the files structured like the above are;

* `read_ctrlpts(file_name)` for files containing _(x, y)_ style control points.
* `read_ctrlptsw(file_name)` for files containing _(x\*w, y\*w, w)_ style weighted control points.

## Surfaces

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

The format of the weighted control points file is;

| | u0 | u1 | u2 | u3 | u4 | u5 | u6 | u7 | u8 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **v0** | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ |
| **v1** | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ |
| **v2** | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ |
| **v3** | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ |
| **v4** | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ |
| **v5** | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ |
| **v6** | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ |
| **v7** | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ |
| **v8** | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ | _(x\*w, y\*w, z\*w, w)_ |

The methods to read control points from the files structured like the above are

* `read_ctrlpts(file_name)` for files containing _(x, y, z)_ style control points.
* `read_ctrlptsw(file_name)` for files containing _(x\*w, y\*w, z\*w, w)_ style weighted control points.

**Note:** The file formats correspond to a right-handed coordinate system.
