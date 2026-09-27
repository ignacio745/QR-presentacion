import marimo

__generated_with = "0.23.15"
app = marimo.App(
    width="medium",
    layout_file="layouts/presentacion_qr.slides.json",
)


@app.cell
def _():
    import marimo as mo
    import qrcode
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, FancyArrowPatch
    from matplotlib.collections import PatchCollection
    import io
    import base64
    return Rectangle, io, mo, plt, qrcode


@app.cell
def _(qrcode):
    def get_qr_matrix(data, version=2):
        qr = qrcode.QRCode(
            version=version,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=0,
        )
        qr.add_data(data)
        qr.make(fit=False)
        matrix = qr.modules
        return matrix

    def get_finder_pattern_coords():
        coords = set()
        for r in range(7):
            for c in range(7):
                coords.add((r, c))
                coords.add((r, c + 18))
                coords.add((r + 18, c))
        return coords

    def get_separator_coords():
        coords = set()
        for i in range(8):
            coords.add((7, i))
            coords.add((i, 7))
            coords.add((7, i + 17))
            coords.add((i, 17))
            coords.add((17, i))
            coords.add((i + 17, 7))
        coords.add((7, 7))
        coords.add((7, 17))
        coords.add((17, 7))
        coords.add((17, 17))
        return coords

    def get_alignment_pattern_coords():
        coords = set()
        for r in range(16, 21):
            for c in range(16, 21):
                coords.add((r, c))
        return coords

    def get_version_info_coords():
        coords = set()
        for r in range(34, 37):
            for c in range(6):
                coords.add((r, c))
                coords.add((c, r))
        return coords

    def get_timing_pattern_coords():
        coords = set()
        for i in range(8, 17):
            coords.add((6, i))
            coords.add((i, 6))
        return coords

    def get_format_info_coords():
        coords = set()
        for i in range(9):
            if i != 6:
                coords.add((8, i))
                coords.add((i, 8))
        for i in range(17, 25):
            coords.add((8, i))
            if i != 17:
                coords.add((i, 8))
        return coords

    def get_dark_module_coords():
        return {(17, 8)}

    def get_function_pattern_coords():
        coords = set()
        coords.update(get_finder_pattern_coords())
        coords.update(get_separator_coords())
        coords.update(get_alignment_pattern_coords())
        coords.update(get_timing_pattern_coords())
        coords.update(get_format_info_coords())
        coords.update(get_dark_module_coords())
        return coords

    def get_zigzag_path(matrix):
        size = len(matrix)
        function_coords = get_function_pattern_coords()
        path = []
        col = size - 1
        going_up = True
        while col >= 0:
            if col == 6:
                col -= 1
                continue
            if going_up:
                rows = range(size - 1, -1, -1)
            else:
                rows = range(0, size)
            for row in rows:
                for c in [col, col - 1]:
                    if c >= 0 and (row, c) not in function_coords:
                        path.append((row, c))
            going_up = not going_up
            col -= 2
        return path

    def get_data_bits(data, version=2):
        qr = qrcode.QRCode(
            version=version,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=0,
        )
        qr.add_data(data)
        qr.make(fit=False)
        data_cache = qr.data_cache
        bits = []
        for byte in data_cache[:34]:
            for i in range(7, -1, -1):
                bits.append((byte >> i) & 1)
        return bits

    def get_error_correction_bits(data, version=2):
        qr = qrcode.QRCode(
            version=version,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=0,
        )
        qr.add_data(data)
        qr.make(fit=False)
        data_cache = qr.data_cache
        bits = []
        for byte in data_cache[34:44]:
            for i in range(7, -1, -1):
                bits.append((byte >> i) & 1)
        return bits

    def get_format_info_original_bits():
        # Bits en el QR (después de XOR): 111110110101010
        qr_bits = [1,1,1,1,1,0,1,1,0,1,0,1,0,1,0]
        # Máscara XOR: 101010000010010
        mask = [1,0,1,0,1,0,0,0,0,0,1,0,0,1,0]
        # XOR para obtener bits originales
        return [q ^ m for q, m in zip(qr_bits, mask)]

    def get_format_info_positions():
        # Posiciones de los 15 bits del format information
        # Primera copia: alrededor del finder pattern superior izquierdo
        # Segunda copia: fila 8 (bits 0-7) y columna 8 (bits 8-14)
        positions = {
            0: [(0, 8), (8, 24)],
            1: [(1, 8), (8, 23)],
            2: [(2, 8), (8, 22)],
            3: [(3, 8), (8, 21)],
            4: [(4, 8), (8, 20)],
            5: [(5, 8), (8, 19)],
            6: [(7, 8), (8, 18)],
            7: [(8, 8), (8, 17)],
            8: [(8, 7), (18, 8)],
            9: [(8, 5), (19, 8)],
            10: [(8, 4), (20, 8)],
            11: [(8, 3), (21, 8)],
            12: [(8, 2), (22, 8)],
            13: [(8, 1), (23, 8)],
            14: [(8, 0), (24, 8)],
        }
        return positions

    def get_format_info_bits_from_matrix(matrix):
        # Extrae los 15 bits del format info directamente del QR generado
        positions = get_format_info_positions()
        bits = []
        for bit_idx in range(15):
            r, c = positions[bit_idx][0]
            bits.append(1 if matrix[r][c] else 0)
        return bits

    def get_qr_matrix_with_mask(data, mask, version=2):
        qr = qrcode.QRCode(
            version=version,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=0,
            mask_pattern=mask,
        )
        qr.add_data(data)
        qr.make(fit=False)
        return qr.modules

    def get_mask_matrix(mask, size=25):
        matrix = [[False for _ in range(size)] for _ in range(size)]
        for r in range(size):
            for c in range(size):
                if mask == 0:
                    matrix[r][c] = (r + c) % 2 == 0
                elif mask == 1:
                    matrix[r][c] = r % 2 == 0
                elif mask == 2:
                    matrix[r][c] = c % 3 == 0
                elif mask == 3:
                    matrix[r][c] = (r + c) % 3 == 0
                elif mask == 4:
                    matrix[r][c] = (r // 2 + c // 3) % 2 == 0
                elif mask == 5:
                    matrix[r][c] = (r * c) % 2 + (r * c) % 3 == 0
                elif mask == 6:
                    matrix[r][c] = ((r * c) % 2 + (r * c) % 3) % 2 == 0
                elif mask == 7:
                    matrix[r][c] = ((r * c) % 3 + (r + c) % 2) % 2 == 0
        return matrix
    return (
        get_alignment_pattern_coords,
        get_data_bits,
        get_error_correction_bits,
        get_finder_pattern_coords,
        get_format_info_bits_from_matrix,
        get_format_info_coords,
        get_format_info_original_bits,
        get_format_info_positions,
        get_mask_matrix,
        get_qr_matrix,
        get_qr_matrix_with_mask,
        get_timing_pattern_coords,
        get_version_info_coords,
        get_zigzag_path,
    )


@app.cell
def _(Rectangle, io, plt):
    def render_qr(matrix, color_map=None, title=None, show_grid=False, show_arrows=False, arrow_path=None):
        size = len(matrix)
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_xlim(0, size)
        ax.set_ylim(0, size)
        ax.set_aspect('equal')
        ax.invert_yaxis()

        if color_map is None:
            color_map = {}

        for r in range(size):
            for c in range(size):
                if (r, c) in color_map:
                    color = color_map[(r, c)]
                elif matrix[r][c]:
                    color = 'black'
                else:
                    color = 'white'
                
                rect = Rectangle((c, r), 1, 1, facecolor=color, edgecolor='gray' if show_grid else 'none', linewidth=0.5 if show_grid else 0)
                ax.add_patch(rect)

        if show_arrows and arrow_path:
            for i in range(len(arrow_path) - 1):
                r1, c1 = arrow_path[i]
                r2, c2 = arrow_path[i + 1]
                ax.annotate('', xy=(c2 + 0.5, r2 + 0.5), xytext=(c1 + 0.5, r1 + 0.5),
                           arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))

        if title:
            ax.set_title(title, fontsize=16, pad=20)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        buf.seek(0)
        return buf.getvalue()

    return (render_qr,)


@app.cell
def _(get_qr_matrix, mo, render_qr):
    _url = "https://github.com/ignacio745/QR-presentacion"
    _matrix = get_qr_matrix(_url, version=3)
    _img_data = render_qr(_matrix, title="QR del Repositorio")
    _b64 = __import__('base64').b64encode(_img_data).decode()
    mo.md(f"""
    # Códigos QR

    ## Ignacio Benemérito

    ---

    <div style="text-align: center;">
        <img src="data:image/png;base64,{_b64}" width="300" />
        <p><a href="{_url}">{_url}</a></p>
    </div>
    """)
    return


@app.cell
def _(get_qr_matrix, mo, render_qr):
    _matrix = get_qr_matrix("Ignacio Benemerito", version=2)
    _img_data = render_qr(_matrix, title="QR Version 2 - 'Ignacio Benemerito'")
    mo.image(src=f"data:image/png;base64,{__import__('base64').b64encode(_img_data).decode()}", width=400)
    return


@app.cell
def _(
    get_alignment_pattern_coords,
    get_finder_pattern_coords,
    get_qr_matrix,
    mo,
    render_qr,
):
    _matrix = get_qr_matrix("Ignacio Benemerito", version=2)
    _finder_coords = get_finder_pattern_coords()
    _alignment_coords = get_alignment_pattern_coords()

    _color_map = {}
    for _r, _c in _finder_coords:
        if _matrix[_r][_c]:
            _color_map[(_r, _c)] = 'blue'
        else:
            _color_map[(_r, _c)] = 'yellow'

    for _r, _c in _alignment_coords:
        if _matrix[_r][_c]:
            _color_map[(_r, _c)] = 'blue'
        else:
            _color_map[(_r, _c)] = 'yellow'

    _img_data = render_qr(_matrix, color_map=_color_map, title="Patrones de Posición y Alineación")
    mo.image(src=f"data:image/png;base64,{__import__('base64').b64encode(_img_data).decode()}", width=400)
    return


@app.cell
def _(get_qr_matrix, get_timing_pattern_coords, mo, render_qr):
    _matrix = get_qr_matrix("Ignacio Benemerito", version=2)
    _timing_coords = get_timing_pattern_coords()

    _color_map = {}
    for _r, _c in _timing_coords:
        if _matrix[_r][_c]:
            _color_map[(_r, _c)] = 'blue'
        else:
            _color_map[(_r, _c)] = 'yellow'

    _img_data = render_qr(_matrix, color_map=_color_map, title="Timing Strips (Patrones de Temporización)")
    mo.image(src=f"data:image/png;base64,{__import__('base64').b64encode(_img_data).decode()}", width=400)
    return


@app.cell
def _(get_format_info_coords, get_qr_matrix, mo, render_qr):
    _matrix = get_qr_matrix("Ignacio Benemerito", version=2)
    _format_coords = get_format_info_coords()

    _color_map = {}
    for _r, _c in _format_coords:
        _color_map[(_r, _c)] = 'red'

    _img_data = render_qr(_matrix, color_map=_color_map, title="Format Information (Información de Formato)")
    mo.image(src=f"data:image/png;base64,{__import__('base64').b64encode(_img_data).decode()}", width=400)
    return


@app.cell
def _(get_format_info_original_bits, get_format_info_positions, get_qr_matrix, mo, render_qr):
    _matrix = get_qr_matrix("Ignacio Benemerito", version=2)
    _format_coords = get_format_info_coords()
    _original_bits = get_format_info_original_bits()
    _positions = get_format_info_positions()
    
    _color_map = {}
    for _bit_idx in range(13, 15):
        _bit_val = _original_bits[14 - _bit_idx]
        for _r, _c in _positions[_bit_idx]:
            _color = 'blue' if _bit_val == 1 else 'yellow'
            _color_map[(_r, _c)] = _color
    
    for _r, _c in _format_coords:
        if (_r, _c) not in _color_map:
            _color_map[(_r, _c)] = '#d0d0d0'
    
    _img_data = render_qr(_matrix, color_map=_color_map, title="Error Correction Level (Nivel de Corrección de Errores)")
    mo.image(src=f"data:image/png;base64,{__import__('base64').b64encode(_img_data).decode()}", width=400)
    return


@app.cell
def _(get_format_info_original_bits, get_format_info_positions, get_qr_matrix, mo, render_qr):
    _matrix = get_qr_matrix("Ignacio Benemerito", version=2)
    _format_coords = get_format_info_coords()
    _original_bits = get_format_info_original_bits()
    _positions = get_format_info_positions()
    
    _color_map = {}
    for _bit_idx in range(13, 15):
        _bit_val = _original_bits[14 - _bit_idx]
        for _r, _c in _positions[_bit_idx]:
            _color = 'black' if _bit_val == 1 else 'white'
            _color_map[(_r, _c)] = _color
    
    for _bit_idx in range(10, 13):
        _bit_val = _original_bits[14 - _bit_idx]
        for _r, _c in _positions[_bit_idx]:
            _color = 'blue' if _bit_val == 1 else 'yellow'
            _color_map[(_r, _c)] = _color
    
    for _r, _c in _format_coords:
        if (_r, _c) not in _color_map:
            _color_map[(_r, _c)] = '#d0d0d0'
    
    _img_data = render_qr(_matrix, color_map=_color_map, title="Mask Pattern (Patrón de Máscara)")
    mo.image(src=f"data:image/png;base64,{__import__('base64').b64encode(_img_data).decode()}", width=400)
    return


@app.cell
def _(get_format_info_original_bits, get_format_info_positions, get_qr_matrix, mo, render_qr):
    _matrix = get_qr_matrix("Ignacio Benemerito", version=2)
    _format_coords = get_format_info_coords()
    _original_bits = get_format_info_original_bits()
    _positions = get_format_info_positions()
    
    _color_map = {}
    for _bit_idx in range(10, 15):
        _bit_val = _original_bits[14 - _bit_idx]
        for _r, _c in _positions[_bit_idx]:
            _color = 'black' if _bit_val == 1 else 'white'
            _color_map[(_r, _c)] = _color
    
    for _bit_idx in range(0, 10):
        _bit_val = _original_bits[14 - _bit_idx]
        for _r, _c in _positions[_bit_idx]:
            _color = 'blue' if _bit_val == 1 else 'yellow'
            _color_map[(_r, _c)] = _color
    
    _img_data = render_qr(_matrix, color_map=_color_map, title="BCH Code (Código de Corrección de Errores)")
    _b64 = __import__('base64').b64encode(_img_data).decode()
    
    mo.md(f"""
<div style="display: flex; justify-content: space-around; align-items: flex-start; gap: 20px;">
    <div style="text-align: center; flex: 0 0 400px;">
        <img src="data:image/png;base64,{_b64}" width="400" />
    </div>
    <div style="text-align: left; flex: 1; font-family: monospace; font-size: 13px; line-height: 1.6;">
        <h3 style="margin-top: 0;">Cálculo BCH (15, 5)</h3>
        
        <p><strong>1. Bits de datos (5 bits):</strong></p>
        <div style="margin-left: 20px;">
            Nivel EC: L → <span style="color: black; font-weight: bold;">01</span><br>
            Máscara: 2 → <span style="color: black; font-weight: bold;">010</span><br>
            Datos: <span style="color: black; font-weight: bold;">01010</span>
        </div>
        
        <p><strong>2. Polinomio de datos:</strong></p>
        <div style="margin-left: 20px;">
            01010 → X³ + X
        </div>
        
        <p><strong>3. Elevar a X¹⁰ (shift de 10 posiciones):</strong></p>
        <div style="margin-left: 20px;">
            (X³ + X) · X¹⁰ = X¹³ + X¹¹
        </div>
        
        <p><strong>4. Polinomio generador G(x):</strong></p>
        <div style="margin-left: 20px;">
            X¹⁰ + X⁸ + X⁵ + X⁴ + X² + X + 1
        </div>
        
        <p><strong>5. División en GF(2):</strong></p>
        <div style="margin-left: 20px; background: #f5f5f5; padding: 10px; border-radius: 4px;">
            <div>X¹³ + X¹¹</div>
            <div>÷ G(x)·X³ = X¹³+X¹¹+X⁸+X⁷+X⁵+X⁴+X³</div>
            <div style="border-top: 2px solid #333; margin: 4px 0;"></div>
            <div>Resto = X⁸ + X⁷ + X⁵ + X⁴ + X³</div>
        </div>
        
        <p><strong>6. Bits BCH (10 bits):</strong></p>
        <div style="margin-left: 20px;">
            <span style="color: blue; font-weight: bold;">0110111000</span>
        </div>
        
        <p><strong>7. Concatenar datos + BCH:</strong></p>
        <div style="margin-left: 20px; background: #e8f5e9; padding: 10px; border-radius: 4px;">
            <span style="color: black; font-weight: bold;">01010</span> + 
            <span style="color: blue; font-weight: bold;">0110111000</span> = 
            <span style="color: green; font-weight: bold;">010100110111000</span>
        </div>
    </div>
</div>
    """)
    return


@app.cell
def _(get_format_info_bits_from_matrix, get_format_info_original_bits, get_format_info_positions, get_qr_matrix, mo, render_qr):
    _matrix = get_qr_matrix("Ignacio Benemerito", version=2)
    _original_bits = get_format_info_original_bits()
    _positions = get_format_info_positions()
    
    _matrix_before = [row[:] for row in _matrix]
    _matrix_after = [row[:] for row in _matrix]
    
    _xor_bits = get_format_info_bits_from_matrix(_matrix)
    
    _color_map_before = {}
    for _bit_idx in range(15):
        _bit_val = _original_bits[14 - _bit_idx]
        _color = 'blue' if _bit_val == 1 else 'yellow'
        for _r, _c in _positions[_bit_idx]:
            _matrix_before[_r][_c] = bool(_bit_val)
            _color_map_before[(_r, _c)] = _color
    
    _color_map_after = {}
    for _bit_idx in range(15):
        _bit_val = _xor_bits[_bit_idx]
        _color = 'blue' if _bit_val == 1 else 'yellow'
        for _r, _c in _positions[_bit_idx]:
            _matrix_after[_r][_c] = bool(_bit_val)
            _color_map_after[(_r, _c)] = _color
    
    _img_before = render_qr(_matrix_before, color_map=_color_map_before, title="Antes de XOR (bits originales)")
    _img_after = render_qr(_matrix_after, color_map=_color_map_after, title="Después de XOR (bits almacenados)")
    
    _b64_before = __import__('base64').b64encode(_img_before).decode()
    _b64_after = __import__('base64').b64encode(_img_after).decode()
    
    _original_str = ''.join(map(str, _original_bits))
    _xor_mask_str = '101010000010010'
    _result_str = ''.join(map(str, reversed(_xor_bits)))
    
    mo.md(f"""
<div style="display: flex; justify-content: space-around; align-items: flex-start; gap: 20px;">
    <div style="text-align: center; flex: 0 0 350px;">
        <img src="data:image/png;base64,{_b64_before}" width="350" />
    </div>
    <div style="text-align: center; flex: 0 0 280px; font-family: monospace; font-size: 14px; line-height: 1.8; padding-top: 150px;">
        <div style="background: #f5f5f5; padding: 15px; border-radius: 8px;">
            <div style="color: black; font-weight: bold;">{_original_str}</div>
            <div style="color: #666; font-size: 12px;">⊕ XOR</div>
            <div style="color: blue; font-weight: bold;">{_xor_mask_str}</div>
            <div style="border-top: 2px solid #333; margin: 8px 0;"></div>
            <div style="color: green; font-weight: bold;">{_result_str}</div>
        </div>
    </div>
    <div style="text-align: center; flex: 0 0 350px;">
        <img src="data:image/png;base64,{_b64_after}" width="350" />
    </div>
</div>
    """)
    return


@app.cell
def _(get_qr_matrix, get_zigzag_path, mo, render_qr):
    _matrix = get_qr_matrix("Ignacio Benemerito", version=2)
    _zigzag_path = get_zigzag_path(_matrix)

    _color_map = {}
    for _r, _c in _zigzag_path:
        _color_map[(_r, _c)] = 'white'

    if _zigzag_path:
        _first_r, _first_c = _zigzag_path[0]
        _color_map[(_first_r, _first_c)] = 'red'

    _img_data = render_qr(_matrix, color_map=_color_map, title="Patrón Zigzag de Almacenamiento de Datos", 
                         show_grid=True, show_arrows=True, arrow_path=_zigzag_path)
    mo.image(src=f"data:image/png;base64,{__import__('base64').b64encode(_img_data).decode()}", width=400)
    return


@app.cell
def _(get_data_bits, get_qr_matrix, get_zigzag_path, mo, render_qr):
    _matrix = get_qr_matrix("Ignacio Benemerito", version=2)
    _zigzag_path = get_zigzag_path(_matrix)
    _data_bits = get_data_bits("Ignacio Benemerito", version=2)
    
    _color_map = {}
    for _i in range(4):
        if _i < len(_zigzag_path):
            _r, _c = _zigzag_path[_i]
            _bit_val = _data_bits[_i]
            _color = 'blue' if _bit_val == 1 else 'yellow'
            _color_map[(_r, _c)] = _color
    
    for _i in range(4, len(_zigzag_path)):
        _r, _c = _zigzag_path[_i]
        _color_map[(_r, _c)] = 'white'
    
    _img_data = render_qr(_matrix, color_map=_color_map, title="Mode Indicator (Modo de Codificación)")
    _b64 = __import__('base64').b64encode(_img_data).decode()
    
    mo.md(f"""
<div style="display: flex; justify-content: space-around; align-items: flex-start; gap: 20px;">
    <div style="text-align: center; flex: 0 0 400px;">
        <img src="data:image/png;base64,{_b64}" width="400" />
    </div>
    <div style="text-align: left; flex: 1; font-family: monospace; font-size: 14px; padding-top: 100px;">
        <h3>Modos de Codificación</h3>
        <table style="border-collapse: collapse; margin-top: 20px;">
            <tr>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: center;">Binario</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Modo</th>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">0001</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Numérico</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">0010</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Alfanumérico</td>
            </tr>
            <tr style="background-color: #e8f5e9; font-weight: bold;">
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">0100</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Byte de 8 bits ←</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">1000</td>
                <td style="padding: 8px; border: 1px solid #ddd;">Kanji</td>
            </tr>
        </table>
    </div>
</div>
""")
    return


@app.cell
def _(get_data_bits, get_qr_matrix, get_zigzag_path, mo, render_qr):
    _matrix = get_qr_matrix("Ignacio Benemerito", version=2)
    _zigzag_path = get_zigzag_path(_matrix)
    _data_bits = get_data_bits("Ignacio Benemerito", version=2)
    
    _color_map = {}
    for _i in range(4):
        if _i < len(_zigzag_path):
            _r, _c = _zigzag_path[_i]
            _bit_val = _data_bits[_i]
            _color = 'black' if _bit_val == 1 else 'white'
            _color_map[(_r, _c)] = _color
    
    for _i in range(4, 12):
        if _i < len(_zigzag_path):
            _r, _c = _zigzag_path[_i]
            _bit_val = _data_bits[_i]
            _color = 'blue' if _bit_val == 1 else 'yellow'
            _color_map[(_r, _c)] = _color
    
    for _i in range(12, len(_zigzag_path)):
        _r, _c = _zigzag_path[_i]
        _color_map[(_r, _c)] = 'white'
    
    _img_data = render_qr(_matrix, color_map=_color_map, title="Character Count (Contador de Caracteres)")
    _b64 = __import__('base64').b64encode(_img_data).decode()
    
    mo.md(f"""
<div style="display: flex; justify-content: space-around; align-items: flex-start; gap: 20px;">
    <div style="text-align: center; flex: 0 0 400px;">
        <img src="data:image/png;base64,{_b64}" width="400" />
    </div>
    <div style="text-align: left; flex: 1; font-family: monospace; font-size: 14px; padding-top: 100px;">
        <h3>Contador de Caracteres</h3>
        <div style="margin-top: 20px;">
            <p><strong>Texto:</strong> "Ignacio Benemerito"</p>
            <p><strong>Cantidad de caracteres:</strong></p>
            <div style="margin-left: 20px; margin-top: 10px; padding: 15px; background-color: #f5f5f5; border-radius: 5px;">
                <p><strong>Decimal:</strong> 18</p>
                <p><strong>Binario:</strong> <span style="color: blue; font-weight: bold;">00010010</span></p>
            </div>
        </div>
    </div>
</div>
""")
    return


@app.cell
def _(get_data_bits, get_function_pattern_coords, get_qr_matrix, get_zigzag_path, mo):
    _matrix = get_qr_matrix("Ignacio Benemerito", version=2)
    _zigzag_path = get_zigzag_path(_matrix)
    _data_bits = get_data_bits("Ignacio Benemerito", version=2)
    _function_coords = get_function_pattern_coords()
    
    _matrix_list = [[1 if _matrix[_r][_c] else 0 for _c in range(len(_matrix[0]))] for _r in range(len(_matrix))]
    _zigzag_list = [[_r, _c] for _r, _c in _zigzag_path]
    _function_coords_list = list(_function_coords)
    
    _text = "Ignacio Benemerito"
    _char_bits = []
    for _ch in _text:
        _byte_val = ord(_ch)
        _bits = []
        for _i in range(7, -1, -1):
            _bits.append((_byte_val >> _i) & 1)
        _char_bits.append(_bits)
    
    _html = f"""
    <div style="text-align: center; font-family: monospace;">
        <canvas id="qr-canvas" width="400" height="400" style="border: 1px solid #ccc; image-rendering: pixelated;"></canvas>
        <div id="text-display" style="font-size: 24px; margin: 20px 0; letter-spacing: 2px;"></div>
        <div id="bits-display" style="font-size: 14px; margin: 10px 0; line-height: 1.8;"></div>
        <div id="bit-info" style="font-size: 16px; margin: 15px 0; color: #333;"></div>
        <div style="margin: 20px 0;">
            <button onclick="reset()" style="padding: 8px 16px; margin: 0 5px;">⏮</button>
            <button onclick="stepBack()" style="padding: 8px 16px; margin: 0 5px;">◀</button>
            <button onclick="togglePlay()" id="play-btn" style="padding: 8px 16px; margin: 0 5px;">▶</button>
            <button onclick="stepForward()" style="padding: 8px 16px; margin: 0 5px;">▶</button>
            <button onclick="jumpToEnd()" style="padding: 8px 16px; margin: 0 5px;">⏭</button>
            <select id="speed-select" onchange="changeSpeed()" style="padding: 8px; margin-left: 20px;">
                <option value="200">Lento</option>
                <option value="100" selected>Normal</option>
                <option value="50">Rápido</option>
            </select>
        </div>
        <div style="margin: 15px 0;">
            <input type="range" id="progress" min="0" max="271" value="0" style="width: 80%;" onchange="seekTo(this.value)" />
        </div>
    </div>
    <script>
        const canvas = document.getElementById('qr-canvas');
        const ctx = canvas.getContext('2d');
        const moduleSize = 16;
        
        const matrix = {str(_matrix_list)};
        const zigzagPath = {str(_zigzag_list)};
        const dataBits = {str(_data_bits)};
        const functionCoords = new Set({str(_function_coords_list)}.map(c => c[0] + ',' + c[1]));
        const text = "{_text}";
        const charBits = {str(_char_bits)};
        
        const finderPatternCoords = new Set();
        for (let r = 0; r < 7; r++) {{
            for (let c = 0; c < 7; c++) {{
                finderPatternCoords.add(r + ',' + c);
                finderPatternCoords.add(r + ',' + (c + 18));
                finderPatternCoords.add((r + 18) + ',' + c);
            }}
        }}
        const alignmentPatternCoords = new Set();
        for (let r = 16; r <= 20; r++) {{
            for (let c = 16; c <= 20; c++) {{
                alignmentPatternCoords.add(r + ',' + c);
            }}
        }}
        const timingStripCoords = new Set();
        for (let i = 8; i <= 16; i++) {{
            timingStripCoords.add('6,' + i);
            timingStripCoords.add(i + ',6');
        }}
        const formatStripCoords = new Set();
        for (let i = 0; i <= 8; i++) {{
            if (i !== 6) {{
                formatStripCoords.add('8,' + i);
                formatStripCoords.add(i + ',8');
            }}
        }}
        for (let i = 17; i <= 24; i++) {{
            formatStripCoords.add('8,' + i);
        }}
        for (let i = 18; i <= 24; i++) {{
            formatStripCoords.add(i + ',8');
        }}
        const darkModuleCoords = new Set(['17,8']);
        
        let currentBit = 0;
        let playing = false;
        let intervalId = null;
        let speed = 100;
        
        function renderFrame() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            for (let r = 0; r < 25; r++) {{
                for (let c = 0; c < 25; c++) {{
                    const key = r + ',' + c;
                    const isFinder = finderPatternCoords.has(key);
                    const isAlignment = alignmentPatternCoords.has(key);
                    const isTiming = timingStripCoords.has(key);
                    const isFormat = formatStripCoords.has(key);
                    const isDarkModule = darkModuleCoords.has(key);
                    
                    if (isDarkModule) {{
                        ctx.fillStyle = 'pink';
                        ctx.fillRect(c * moduleSize, r * moduleSize, moduleSize, moduleSize);
                    }} else if (isFinder || isAlignment || isTiming || isFormat) {{
                        ctx.fillStyle = matrix[r][c] === 1 ? 'blue' : 'yellow';
                        ctx.fillRect(c * moduleSize, r * moduleSize, moduleSize, moduleSize);
                    }} else if (functionCoords.has(key)) {{
                        ctx.fillStyle = matrix[r][c] === 1 ? '#d0d0d0' : '#f0f0f0';
                        ctx.fillRect(c * moduleSize, r * moduleSize, moduleSize, moduleSize);
                    }}
                }}
            }}
            
            for (let i = 0; i <= currentBit; i++) {{
                if (i < zigzagPath.length) {{
                    const [r, c] = zigzagPath[i];
                    const bit = dataBits[i];
                    
                    if (i === currentBit) {{
                        ctx.fillStyle = '#00ff00';
                    }} else {{
                        ctx.fillStyle = bit === 1 ? 'black' : 'white';
                    }}
                    
                    ctx.fillRect(c * moduleSize, r * moduleSize, moduleSize, moduleSize);
                    ctx.strokeStyle = 'gray';
                    ctx.lineWidth = 0.5;
                    ctx.strokeRect(c * moduleSize, r * moduleSize, moduleSize, moduleSize);
                }}
            }}
        }}
        
        function updateDisplay() {{
            renderFrame();
            document.getElementById('progress').value = currentBit;
            
            let textHtml = '';
            let bitsHtml = '';
            
            const modeBits = 4;
            const countBits = 8;
            const dataStartBit = modeBits + countBits;
            
            if (currentBit < dataStartBit) {{
                for (let i = 0; i < text.length; i++) {{
                    textHtml += '<span style="color: #ccc;">' + text[i] + '</span>';
                }}
                for (let i = 0; i < text.length; i++) {{
                    bitsHtml += '<div style="color: #ccc; display: inline-block; margin: 0 10px;">' + text[i] + ': ' + charBits[i].join('') + '</div>';
                }}
            }} else {{
                const charBitIndex = currentBit - dataStartBit;
                const currentCharIndex = Math.floor(charBitIndex / 8);
                const currentBitInChar = charBitIndex % 8;
                
                for (let i = 0; i < text.length; i++) {{
                    let color = '#ccc';
                    if (i < currentCharIndex) {{
                        color = 'black';
                    }} else if (i === currentCharIndex) {{
                        color = 'red';
                    }}
                    textHtml += '<span style="color: ' + color + ';">' + text[i] + '</span>';
                }}
                
                for (let i = 0; i < text.length; i++) {{
                    let bitsStr = '';
                    for (let j = 0; j < 8; j++) {{
                        let bitColor = '#ccc';
                        if (i < currentCharIndex) {{
                            bitColor = 'black';
                        }} else if (i === currentCharIndex) {{
                            if (j < currentBitInChar) {{
                                bitColor = 'black';
                            }} else if (j === currentBitInChar) {{
                                bitColor = 'red';
                            }}
                        }}
                        bitsStr += '<span style="color: ' + bitColor + ';">' + charBits[i][j] + '</span>';
                    }}
                    bitsHtml += '<div style="display: inline-block; margin: 0 10px;">' + text[i] + ': ' + bitsStr + '</div>';
                }}
            }}
            
            document.getElementById('text-display').innerHTML = textHtml;
            document.getElementById('bits-display').innerHTML = bitsHtml;
            
            let info = 'Bit ' + (currentBit + 1) + '/272';
            if (currentBit < 4) {{
                info += ' - Mode Indicator';
            }} else if (currentBit < 12) {{
                info += ' - Character Count';
            }} else if (currentBit < 156) {{
                const charIdx = Math.floor((currentBit - 12) / 8);
                info += ' - Carácter "' + text[charIdx] + '" (' + text.charCodeAt(charIdx) + ')';
            }} else if (currentBit < 160) {{
                info += ' - Terminador';
            }} else {{
                info += ' - Padding';
            }}
            document.getElementById('bit-info').innerHTML = info;
        }}
        
        function play() {{
            playing = true;
            document.getElementById('play-btn').textContent = '⏸';
            intervalId = setInterval(() => {{
                if (currentBit < 271) {{
                    currentBit++;
                    updateDisplay();
                }} else {{
                    pause();
                }}
            }}, speed);
        }}
        
        function pause() {{
            playing = false;
            document.getElementById('play-btn').textContent = '▶';
            clearInterval(intervalId);
        }}
        
        function togglePlay() {{
            if (playing) {{
                pause();
            }} else {{
                play();
            }}
        }}
        
        function stepForward() {{
            if (currentBit < 271) {{
                currentBit++;
                updateDisplay();
            }}
        }}
        
        function stepBack() {{
            if (currentBit > 0) {{
                currentBit--;
                updateDisplay();
            }}
        }}
        
        function reset() {{
            pause();
            currentBit = 0;
            updateDisplay();
        }}
        
        function jumpToEnd() {{
            pause();
            currentBit = 271;
            updateDisplay();
        }}
        
        function seekTo(val) {{
            currentBit = parseInt(val);
            updateDisplay();
        }}
        
        function changeSpeed() {{
            speed = parseInt(document.getElementById('speed-select').value);
            if (playing) {{
                pause();
                play();
            }}
        }}
        
        updateDisplay();
    </script>
    """
    
    mo.iframe(_html, width="100%", height="900px")
    return


@app.cell
def _(get_data_bits, get_error_correction_bits, get_function_pattern_coords, get_qr_matrix, get_zigzag_path, mo):
    _matrix = get_qr_matrix("Ignacio Benemerito", version=2)
    _zigzag_path = get_zigzag_path(_matrix)
    _data_bits = get_data_bits("Ignacio Benemerito", version=2)
    _ec_bits = get_error_correction_bits("Ignacio Benemerito", version=2)
    _function_coords = get_function_pattern_coords()
    
    _matrix_list = [[1 if _matrix[_r][_c] else 0 for _c in range(len(_matrix[0]))] for _r in range(len(_matrix))]
    _zigzag_list = [[_r, _c] for _r, _c in _zigzag_path]
    _function_coords_list = list(_function_coords)
    
    _ec_bytes = []
    for _i in range(10):
        _byte_bits = _ec_bits[_i*8:(_i+1)*8]
        _ec_bytes.append(_byte_bits)
    
    _html = f"""
    <div style="text-align: center; font-family: monospace;">
        <canvas id="qr-canvas-ec" width="400" height="400" style="border: 1px solid #ccc; image-rendering: pixelated;"></canvas>
        <div id="bytes-display" style="font-size: 14px; margin: 20px 0; line-height: 1.8;"></div>
        <div id="bit-info" style="font-size: 16px; margin: 15px 0; color: #333;"></div>
        <div style="margin: 20px 0;">
            <button onclick="reset()" style="padding: 8px 16px; margin: 0 5px;">⏮</button>
            <button onclick="stepBack()" style="padding: 8px 16px; margin: 0 5px;">◀</button>
            <button onclick="togglePlay()" id="play-btn" style="padding: 8px 16px; margin: 0 5px;">▶</button>
            <button onclick="stepForward()" style="padding: 8px 16px; margin: 0 5px;">▶</button>
            <button onclick="jumpToEnd()" style="padding: 8px 16px; margin: 0 5px;">⏭</button>
            <select id="speed-select" onchange="changeSpeed()" style="padding: 8px; margin-left: 20px;">
                <option value="200">Lento</option>
                <option value="100" selected>Normal</option>
                <option value="50">Rápido</option>
            </select>
        </div>
        <div style="margin: 15px 0;">
            <input type="range" id="progress" min="0" max="79" value="0" style="width: 80%;" onchange="seekTo(this.value)" />
        </div>
    </div>
    <script>
        const canvas = document.getElementById('qr-canvas-ec');
        const ctx = canvas.getContext('2d');
        const moduleSize = 16;
        
        const matrix = {str(_matrix_list)};
        const zigzagPath = {str(_zigzag_list)};
        const dataBits = {str(_data_bits)};
        const ecBits = {str(_ec_bits)};
        const functionCoords = new Set({str(_function_coords_list)}.map(c => c[0] + ',' + c[1]));
        const ecBytes = {str(_ec_bytes)};
        
        const finderPatternCoords = new Set();
        for (let r = 0; r < 7; r++) {{
            for (let c = 0; c < 7; c++) {{
                finderPatternCoords.add(r + ',' + c);
                finderPatternCoords.add(r + ',' + (c + 18));
                finderPatternCoords.add((r + 18) + ',' + c);
            }}
        }}
        const alignmentPatternCoords = new Set();
        for (let r = 16; r <= 20; r++) {{
            for (let c = 16; c <= 20; c++) {{
                alignmentPatternCoords.add(r + ',' + c);
            }}
        }}
        const timingStripCoords = new Set();
        for (let i = 8; i <= 16; i++) {{
            timingStripCoords.add('6,' + i);
            timingStripCoords.add(i + ',6');
        }}
        const formatStripCoords = new Set();
        for (let i = 0; i <= 8; i++) {{
            if (i !== 6) {{
                formatStripCoords.add('8,' + i);
                formatStripCoords.add(i + ',8');
            }}
        }}
        for (let i = 17; i <= 24; i++) {{
            formatStripCoords.add('8,' + i);
        }}
        for (let i = 18; i <= 24; i++) {{
            formatStripCoords.add(i + ',8');
        }}
        const darkModuleCoords = new Set(['17,8']);
        
        let currentBit = 0;
        let playing = false;
        let intervalId = null;
        let speed = 100;
        
        function renderFrame() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            for (let r = 0; r < 25; r++) {{
                for (let c = 0; c < 25; c++) {{
                    const key = r + ',' + c;
                    const isFinder = finderPatternCoords.has(key);
                    const isAlignment = alignmentPatternCoords.has(key);
                    const isTiming = timingStripCoords.has(key);
                    const isFormat = formatStripCoords.has(key);
                    const isDarkModule = darkModuleCoords.has(key);
                    
                    if (isDarkModule) {{
                        ctx.fillStyle = 'pink';
                        ctx.fillRect(c * moduleSize, r * moduleSize, moduleSize, moduleSize);
                    }} else if (isFinder || isAlignment || isTiming || isFormat) {{
                        ctx.fillStyle = matrix[r][c] === 1 ? 'blue' : 'yellow';
                        ctx.fillRect(c * moduleSize, r * moduleSize, moduleSize, moduleSize);
                    }} else if (functionCoords.has(key)) {{
                        ctx.fillStyle = matrix[r][c] === 1 ? '#d0d0d0' : '#f0f0f0';
                        ctx.fillRect(c * moduleSize, r * moduleSize, moduleSize, moduleSize);
                    }}
                }}
            }}
            
            for (let i = 0; i < dataBits.length; i++) {{
                if (i < zigzagPath.length) {{
                    const [r, c] = zigzagPath[i];
                    const bit = dataBits[i];
                    ctx.fillStyle = bit === 1 ? '#666666' : '#cccccc';
                    ctx.fillRect(c * moduleSize, r * moduleSize, moduleSize, moduleSize);
                    ctx.strokeStyle = 'gray';
                    ctx.lineWidth = 0.5;
                    ctx.strokeRect(c * moduleSize, r * moduleSize, moduleSize, moduleSize);
                }}
            }}
            
            for (let i = 0; i <= currentBit; i++) {{
                const pathIdx = dataBits.length + i;
                if (pathIdx < zigzagPath.length) {{
                    const [r, c] = zigzagPath[pathIdx];
                    const bit = ecBits[i];
                    
                    if (i === currentBit) {{
                        ctx.fillStyle = '#00ff00';
                    }} else {{
                        ctx.fillStyle = bit === 1 ? 'black' : 'white';
                    }}
                    
                    ctx.fillRect(c * moduleSize, r * moduleSize, moduleSize, moduleSize);
                    ctx.strokeStyle = 'gray';
                    ctx.lineWidth = 0.5;
                    ctx.strokeRect(c * moduleSize, r * moduleSize, moduleSize, moduleSize);
                }}
            }}
        }}
        
        function updateDisplay() {{
            renderFrame();
            document.getElementById('progress').value = currentBit;
            
            let bytesHtml = '';
            
            const currentByteIndex = Math.floor(currentBit / 8);
            const currentBitInByte = currentBit % 8;
            
            for (let i = 0; i < ecBytes.length; i++) {{
                let bitsStr = '';
                for (let j = 0; j < 8; j++) {{
                    let bitColor = '#ccc';
                    if (i < currentByteIndex) {{
                        bitColor = 'black';
                    }} else if (i === currentByteIndex) {{
                        if (j < currentBitInByte) {{
                            bitColor = 'black';
                        }} else if (j === currentBitInByte) {{
                            bitColor = 'red';
                        }}
                    }}
                    bitsStr += '<span style="color: ' + bitColor + ';">' + ecBytes[i][j] + '</span>';
                }}
                const byteValue = parseInt(ecBytes[i].join(''), 2);
                bytesHtml += '<div style="display: inline-block; margin: 0 10px;">Byte ' + i + ': ' + bitsStr + ' (' + byteValue + ')</div>';
            }}
            
            document.getElementById('bytes-display').innerHTML = bytesHtml;
            
            let info = 'Bit ' + (272 + currentBit) + '/352';
            info += ' - Error Correction Byte ' + (currentByteIndex + 1) + '/10';
            const byteValue = parseInt(ecBytes[currentByteIndex].join(''), 2);
            info += ' - Valor: ' + ecBytes[currentByteIndex].join('') + ' (' + byteValue + ')';
            document.getElementById('bit-info').innerHTML = info;
        }}
        
        function play() {{
            playing = true;
            document.getElementById('play-btn').textContent = '⏸';
            intervalId = setInterval(() => {{
                if (currentBit < 79) {{
                    currentBit++;
                    updateDisplay();
                }} else {{
                    pause();
                }}
            }}, speed);
        }}
        
        function pause() {{
            playing = false;
            document.getElementById('play-btn').textContent = '▶';
            clearInterval(intervalId);
        }}
        
        function togglePlay() {{
            if (playing) {{
                pause();
            }} else {{
                play();
            }}
        }}
        
        function stepForward() {{
            if (currentBit < 79) {{
                currentBit++;
                updateDisplay();
            }}
        }}
        
        function stepBack() {{
            if (currentBit > 0) {{
                currentBit--;
                updateDisplay();
            }}
        }}
        
        function reset() {{
            pause();
            currentBit = 0;
            updateDisplay();
        }}
        
        function jumpToEnd() {{
            pause();
            currentBit = 79;
            updateDisplay();
        }}
        
        function seekTo(val) {{
            currentBit = parseInt(val);
            updateDisplay();
        }}
        
        function changeSpeed() {{
            speed = parseInt(document.getElementById('speed-select').value);
            if (playing) {{
                pause();
                play();
            }}
        }}
        
        updateDisplay();
    </script>
    """
    
    mo.iframe(_html, width="100%", height="900px")
    return


@app.cell
def _(get_format_info_positions, get_function_pattern_coords, get_mask_matrix, get_qr_matrix_with_mask, mo):
    _text = "Ignacio Benemerito"
    _qr_matrices = []
    _format_info_all = []
    _positions = get_format_info_positions()
    
    for _mask in range(8):
        _matrix = get_qr_matrix_with_mask(_text, _mask, version=2)
        _qr_matrices.append(_matrix)
        _format_bits = []
        for _bit_idx in range(15):
            _r, _c = _positions[_bit_idx][0]
            _format_bits.append(1 if _matrix[_r][_c] else 0)
        _format_info_all.append(_format_bits)
    
    _mask_matrices = []
    for _mask in range(8):
        _mask_matrices.append(get_mask_matrix(_mask, size=25))
    
    _function_coords = get_function_pattern_coords()
    
    _qr_matrices_list = []
    for _matrix in _qr_matrices:
        _matrix_list = [[1 if _matrix[_r][_c] else 0 for _c in range(len(_matrix[0]))] for _r in range(len(_matrix))]
        _qr_matrices_list.append(_matrix_list)
    
    _mask_matrices_list = []
    for _matrix in _mask_matrices:
        _matrix_list = [[1 if _matrix[_r][_c] else 0 for _c in range(len(_matrix[0]))] for _r in range(len(_matrix))]
        _mask_matrices_list.append(_matrix_list)
    
    _function_coords_list = list(_function_coords)
    
    _html = f"""
    <div style="display: flex; justify-content: space-around; align-items: flex-start; gap: 20px; font-family: monospace;">
        <div style="text-align: center; flex: 0 0 400px;">
            <canvas id="qr-canvas-masks" width="400" height="400" style="border: 1px solid #ccc; image-rendering: pixelated;"></canvas>
            <div id="mask-info" style="font-size: 18px; margin: 20px 0; color: #333;"></div>
            <div id="mask-buttons" style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin: 20px 0;">
            </div>
        </div>
        <div style="text-align: left; flex: 1; font-size: 13px; line-height: 1.6;">
            <h3 style="margin-top: 0;">Criterios de Evaluación de Máscaras</h3>
            
            <p><strong>1. Grupos consecutivos (N1):</strong></p>
            <div style="margin-left: 20px; background: #f5f5f5; padding: 10px; border-radius: 4px;">
                5+ módulos del mismo color en fila/columna<br>
                Penalización: 3 + (k - 5) por cada grupo de k módulos
            </div>
            
            <p><strong>2. Bloques 2x2 (N2):</strong></p>
            <div style="margin-left: 20px; background: #f5f5f5; padding: 10px; border-radius: 4px;">
                Bloques de 2x2 módulos del mismo color<br>
                Penalización: 3 puntos por cada bloque
            </div>
            
            <p><strong>3. Patrones tipo finder (N3):</strong></p>
            <div style="margin-left: 20px; background: #f5f5f5; padding: 10px; border-radius: 4px;">
                Secuencias: 1,0,1,1,1,0,1,0,0,0,0 o 0,0,0,0,1,0,1,1,1,0,1<br>
                Penalización: 40 puntos por cada ocurrencia
            </div>
            
            <p><strong>4. Proporción de módulos oscuros (N4):</strong></p>
            <div style="margin-left: 20px; background: #f5f5f5; padding: 10px; border-radius: 4px;">
                Desviación del 50% de módulos oscuros<br>
                Penalización: 10 puntos por cada 5% de desviación
            </div>
        </div>
    </div>
    <script>
        const canvas = document.getElementById('qr-canvas-masks');
        const ctx = canvas.getContext('2d');
        const moduleSize = 16;
        
        const qrMatrices = {str(_qr_matrices_list)};
        const maskMatrices = {str(_mask_matrices_list)};
        const formatInfoAll = {str(_format_info_all)};
        const functionCoords = new Set({str(_function_coords_list)}.map(c => c[0] + ',' + c[1]));
        
        const finderPatternCoords = new Set();
        for (let r = 0; r < 7; r++) {{
            for (let c = 0; c < 7; c++) {{
                finderPatternCoords.add(r + ',' + c);
                finderPatternCoords.add(r + ',' + (c + 18));
                finderPatternCoords.add((r + 18) + ',' + c);
            }}
        }}
        const alignmentPatternCoords = new Set();
        for (let r = 16; r <= 20; r++) {{
            for (let c = 16; c <= 20; c++) {{
                alignmentPatternCoords.add(r + ',' + c);
            }}
        }}
        const timingStripCoords = new Set();
        for (let i = 8; i <= 16; i++) {{
            timingStripCoords.add('6,' + i);
            timingStripCoords.add(i + ',6');
        }}
        const formatStripCoords = new Set();
        for (let i = 0; i <= 8; i++) {{
            if (i !== 6) {{
                formatStripCoords.add('8,' + i);
                formatStripCoords.add(i + ',8');
            }}
        }}
        for (let i = 17; i <= 24; i++) {{
            formatStripCoords.add('8,' + i);
        }}
        for (let i = 18; i <= 24; i++) {{
            formatStripCoords.add(i + ',8');
        }}
        const darkModuleCoords = new Set(['17,8']);
        
        const formatPositions = {{
            0: [[0, 8], [8, 24]],
            1: [[1, 8], [8, 23]],
            2: [[2, 8], [8, 22]],
            3: [[3, 8], [8, 21]],
            4: [[4, 8], [8, 20]],
            5: [[5, 8], [8, 19]],
            6: [[7, 8], [8, 18]],
            7: [[8, 8], [8, 17]],
            8: [[8, 7], [18, 8]],
            9: [[8, 5], [19, 8]],
            10: [[8, 4], [20, 8]],
            11: [[8, 3], [21, 8]],
            12: [[8, 2], [22, 8]],
            13: [[8, 1], [23, 8]],
            14: [[8, 0], [24, 8]]
        }};
        
        const maskFormulas = [];
        
        let currentMask = 0;
        
        function createMaskButtons() {{
            const container = document.getElementById('mask-buttons');
            for (let i = 0; i < 8; i++) {{
                const buttonDiv = document.createElement('div');
                buttonDiv.style.textAlign = 'center';
                
                const buttonCanvas = document.createElement('canvas');
                buttonCanvas.id = 'mask-button-' + i;
                buttonCanvas.width = 50;
                buttonCanvas.height = 50;
                buttonCanvas.style.border = '2px solid #ccc';
                buttonCanvas.style.cursor = 'pointer';
                buttonCanvas.style.imageRendering = 'pixelated';
                buttonCanvas.onclick = () => selectMask(i);
                
                const label = document.createElement('div');
                label.textContent = 'Máscara ' + i;
                label.style.fontSize = '12px';
                label.style.marginTop = '5px';
                
                buttonDiv.appendChild(buttonCanvas);
                buttonDiv.appendChild(label);
                container.appendChild(buttonDiv);
                
                drawMaskButton(i, buttonCanvas);
            }}
        }}
        
        function drawMaskButton(maskIndex, buttonCanvas) {{
            const buttonCtx = buttonCanvas.getContext('2d');
            const buttonModuleSize = 2;
            
            for (let r = 0; r < 25; r++) {{
                for (let c = 0; c < 25; c++) {{
                    buttonCtx.fillStyle = maskMatrices[maskIndex][r][c] === 1 ? 'black' : 'white';
                    buttonCtx.fillRect(c * buttonModuleSize, r * buttonModuleSize, buttonModuleSize, buttonModuleSize);
                }}
            }}
            
            if (maskIndex === currentMask) {{
                buttonCanvas.style.borderColor = '#0066cc';
                buttonCanvas.style.borderWidth = '3px';
            }} else {{
                buttonCanvas.style.borderColor = '#ccc';
                buttonCanvas.style.borderWidth = '2px';
            }}
        }}
        
        function selectMask(maskIndex) {{
            currentMask = maskIndex;
            updateDisplay();
        }}
        
        function renderFrame() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const matrix = qrMatrices[currentMask];
            const formatBits = formatInfoAll[currentMask];
            
            for (let r = 0; r < 25; r++) {{
                for (let c = 0; c < 25; c++) {{
                    const key = r + ',' + c;
                    const isFinder = finderPatternCoords.has(key);
                    const isAlignment = alignmentPatternCoords.has(key);
                    const isTiming = timingStripCoords.has(key);
                    const isFormat = formatStripCoords.has(key);
                    const isDarkModule = darkModuleCoords.has(key);
                    
                    if (isDarkModule) {{
                        ctx.fillStyle = 'black';
                        ctx.fillRect(c * moduleSize, r * moduleSize, moduleSize, moduleSize);
                    }} else if (isFinder || isAlignment || isTiming) {{
                        ctx.fillStyle = matrix[r][c] === 1 ? 'black' : 'white';
                        ctx.fillRect(c * moduleSize, r * moduleSize, moduleSize, moduleSize);
                    }} else if (isFormat) {{
                        let bitIdx = -1;
                        for (let b = 0; b < 15; b++) {{
                            const pos1 = formatPositions[b][0];
                            const pos2 = formatPositions[b][1];
                            if ((pos1[0] === r && pos1[1] === c) || (pos2[0] === r && pos2[1] === c)) {{
                                bitIdx = b;
                                break;
                            }}
                        }}
                        
                        ctx.fillStyle = matrix[r][c] === 1 ? 'black' : 'white';
                        ctx.fillRect(c * moduleSize, r * moduleSize, moduleSize, moduleSize);
                    }} else if (functionCoords.has(key)) {{
                        ctx.fillStyle = matrix[r][c] === 1 ? 'black' : 'white';
                        ctx.fillRect(c * moduleSize, r * moduleSize, moduleSize, moduleSize);
                    }} else {{
                        ctx.fillStyle = matrix[r][c] === 1 ? 'black' : 'white';
                        ctx.fillRect(c * moduleSize, r * moduleSize, moduleSize, moduleSize);
                    }}
                }}
            }}
        }}
        
        function updateDisplay() {{
            renderFrame();
            
            const maskBitValues = ['000', '001', '010', '011', '100', '101', '110', '111'];
            const maskBits = maskBitValues[currentMask];
            let info = 'Máscara activa: ' + currentMask + ' (' + maskBits + ')';
            document.getElementById('mask-info').innerHTML = info;
            
            for (let i = 0; i < 8; i++) {{
                const buttonCanvas = document.getElementById('mask-button-' + i);
                drawMaskButton(i, buttonCanvas);
            }}
        }}
        
        createMaskButtons();
        updateDisplay();
    </script>
    """
    
    mo.iframe(_html, width="100%", height="1000px")
    return


@app.cell
def _(get_qr_matrix, get_version_info_coords, mo, render_qr):
    _matrix = get_qr_matrix("Ignacio Benemerito", version=7)
    _version_coords = get_version_info_coords()
    
    _color_map = {}
    for _r, _c in _version_coords:
        if _matrix[_r][_c]:
            _color_map[(_r, _c)] = 'blue'
        else:
            _color_map[(_r, _c)] = 'yellow'
    
    _img_colored = render_qr(_matrix, color_map=_color_map, title="Información de Versión Resaltada")
    
    _b64_colored = __import__('base64').b64encode(_img_colored).decode()
    
    mo.md(f"""
<div style="display: flex; justify-content: space-around; align-items: flex-start; gap: 20px;">
    <div style="text-align: center; flex: 0 0 400px;">
        <img src="data:image/png;base64,{_b64_colored}" width="400" />
    </div>
    <div style="text-align: left; flex: 1; font-family: monospace; font-size: 13px; line-height: 1.6;">
        <h3 style="margin-top: 0;">Información de Versión</h3>
        <p>Código BCH (18, 6)</p>
    </div>
</div>
    """)
    return


if __name__ == "__main__":
    app.run()
