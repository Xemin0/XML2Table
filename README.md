# XML2Table
A demo python GUI widget meant to facilate the parameter-settings (Contact Energies) in [CompCell3D](https://compucell3d.org/) [Git Page](https://github.com/CompuCell3D/CompuCell3D) using `TkInter`

It simply converts between the copy-pasted XML contents and a visual (upper-triangular) table. XML parsing is done using regular expressions. 

*Could be adapted for other parameter-settings in XML.*

### Required Python Packages
- `TkInter`
- `Numpy`

### How to Use it
Either:
- Copy-paste the contact energy section/plugin from the CC3D generated XML file into the text field on the left
- Start from scratch by adding new cells

Then each button literally does what it says.

### Example Image of the Widget
<img src="./images/example.png">
