### v02_2
- Some visual improvments
- Now the whole table will be recolored based on the current entry's value changes


### Future Features:
- Left-Justified the table (the table starts at the bottom left corner) **Need to handle the visual bugs unless re-rendering the whole frame**
- Make the color bar dynamic and have dots or pins showing the distribution of entry values along the color bar
- A Graph representation (Node-Edge) is probably better visually, but it would require advanced graphical designs

### Major Issues:
#### Juxtapositions of Visual Components
- Relative sizes and minimum allowed sizes (to guarantee showing full texts) are still yet TBD

#### Interactive Logic
- The colors computed are not equally spaced in terms of the relative value between $[0,1]$

#### Code Optimizaiton
- `utils/EventHandler.py` needs to be optimized






----
## Dated

### v02
- Included the whole (symmetric) matrix in the table; 
- Symmetric entries are now dynamically synchronized (both the values and the background color)
- Colored the Entry cells based on the relative values
- Added a static color bar indicating the color range

### v01
- The initial version with a Text Field, several buttons, and a region to create table of entries based on the XML copy-pasted in.
- The table is shown as an upper-triangular matrix
