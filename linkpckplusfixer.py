"""
    Extract .png files to .pck files [Some files maybe corrupted, can't fix that /shrug]
"""

import os
import tqdm

for file in os.listdir('input'):
    count = 0
    with open(os.path.join('input', file), 'rb') as f:
        while True:
            readchunk = f.read(64)
            if readchunk == b'':
                break
            finderpointer = readchunk.find(b'\x89\x50\x4E\x47\x0D\x0A\x1A')
            if finderpointer == -1:
                pass
            else:
                chunk = b''
                f.seek(-64, 1)
                f.seek(finderpointer, 1)
                with tqdm.tqdm(iterable='Bytes') as pbar:
                    while True:
                        readchunk = f.read(64)
                        Iendpointer = readchunk.find(b'\x49\x45\x4E\x44')
                        pbar.update(64)
                        if Iendpointer != -1:
                            f.seek(-64, 1)
                            chunk += f.read(Iendpointer)
                            with open(os.path.join('output', f"{file}{count}.png"), 'wb') as f2:
                                f2.write(chunk)
                                count += 1
                            break
                        elif readchunk == b'':
                            break
                        else:
                            chunk += readchunk
