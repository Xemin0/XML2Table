### v02
- Included the whole (symmetric) matrix in the table; 
- Symmetric entries are now dynamically synchronized (both the values and the background color)
- Colored the Entry cells based on the relative values
- Added a static color bar indicating the color range


### Future Features:
- Left-Justified the table (the table starts at the bottom left corner) **Need to handle the visual bugs unless re-rendering the whole frame**
- Make the color bar dynamic and have dots or pins showing the distribution of entry values along the color bar

### Major Issues:
#### Juxtapositions of Visual Components
- Relative sizes and minimum allowed sizes (to guarantee showing full texts) are still yet TBD

#### Interactive Logic
- The colors computed are not equally spaced in terms of the relative value between $[0,1]$
- The color dynamically assigned is still based on the initial min_max pair
- Entering a new value in an entry does not change the value stored
- Thus, entering a new value only changes the exact synced entry pair, but not other entries.

A workaround is to use the `Convert to XML` button to recollect the values altogether, then `Convert to Table` to color the entries again as a whole.






----
## Dated

### v01
- The initial version with a Text Field, several buttons, and a region to create table of entries based on the XML copy-pasted in.
- The table is shown as an upper-triangular matrix
