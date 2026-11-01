import numpy as np
import pandas as pd
import os
import arcade as aa
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import shutil
import matplotlib.pyplot as plt
import time
import sys

base_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(base_dir)

os.makedirs('runtime', exist_ok=True)
os.makedirs('out', exist_ok=True)
background_path = 'runtime/background.jpg' if os.path.exists('runtime/background.jpg') else 'images/bg.jpg'

start_bc = False
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots(subplot_kw=dict(projection='polar'))
fig4, ax4 = plt.subplots()

def get_scale():
    texture = aa.load_texture(background_path)
    width = texture.width
    scale = 600 / width
    return scale

class Start(aa.View):
    def __init__(self):
        super().__init__()
        self.bg = aa.Sprite(background_path, scale=get_scale())
        self.bg.position = 300, 200
        self.bg_button = aa.Sprite('images/bg_button.png', scale=0.7)
        self.bg_button.position = 550, 350
        self.start_button = aa.Sprite('images/start_button.png', scale=0.7)
        self.start_button.position = 300, 200
        aa.set_background_color(aa.color.SKY_BLUE)
        self.root = tk.Tk()
        self.root.withdraw()
        self.drawts = False

    def on_draw(self):
        self.clear()
        aa.start_render()
        self.bg.draw()
        self.bg_button.draw()
        self.start_button.draw()
        aa.draw_text('统计图生成器', 300, 300, aa.color.WHITE, font_size=40, 
                             font_name=("simhei", "PingFang"), anchor_x="center")
        if start_bc:
            aa.draw_text(f'打开文件{file_path}出错', 300, 200, aa.color.WHITE,
                         font_size=15, font_name=("simhei", "PingFang"), anchor_x="center")
        if self.drawts:
            aa.draw_text('已设置好新背景，重启后可预览', 300, 100, aa.color.WHITE, font_size=15, 
                             font_name=("simhei", "PingFang"), anchor_x="center")

    def on_mouse_release(self, x, y, button, modifiers):
        if self.bg_button.collides_with_point((x, y)):
            old_path = filedialog.askopenfilename(filetypes=[("图片文件", "*.png;*.jpg;*.jpeg;*.gif")])
            new_path = 'runtime/background.jpg'
            try:
                shutil.copy2(old_path, new_path)
                self.drawts = True
                aa.draw_text('已设置好新背景，重启后可预览', 200, 100, aa.color.WHITE, font_size=20, 
                             font_name=("simhei", "PingFang"), anchor_x="center")
            except shutil.SameFileError:
                pass
                
        if self.start_button.collides_with_point((x, y)):
            w.show_view(process)

class Process(aa.View):
    def __init__(self):
        super().__init__()
        self.bg = aa.Sprite(background_path, scale=get_scale())
        self.bg.position = 300, 200
        self.input_file = aa.Sprite('images/common_button.png', scale=2)
        self.input_file.position = 300, 300
        self.input_file.alpha = 120
        
        self.open_line = aa.Sprite('images/common_button.png', scale=2)
        self.open_line.position = 200, 200
        self.open_line.alpha = 120
        self.open_bar = aa.Sprite('images/common_button.png', scale=2)
        self.open_bar.position = 400, 200
        self.open_bar.alpha = 120
        self.open_pie = aa.Sprite('images/common_button.png', scale=2)
        self.open_pie.position = 200, 100
        self.open_pie.alpha = 120
        self.open_radar = aa.Sprite('images/common_button.png', scale=2)
        self.open_radar.position = 400, 100
        self.open_radar.alpha = 120

        self.index_num = 0
        self.show_1, self.show_2, self.show_3, self.show_4 = False, False, False, False

        self.lt1, self.lt2, self.lt3, self.lt4, self.lt = 0, 0, 0, 0, 0
        self.saved1, self.saved2, self.saved3, self.saved4, self.saved = False, False, False, False, False
        self.save_button = aa.Sprite('images/save_button.png', scale=0.7)
        self.save_button.position = 550, 350

        self.continue_button = aa.Sprite('images/continue_button.png', scale=0.7)
        self.continue_button.position = 550, 50

    def on_draw(self):
        self.clear()
        self.bg.draw()
        self.input_file.draw()
        aa.draw_text('导入文件', 300, 300, aa.color.WHITE, font_size=20, 
                             font_name=("simhei", "PingFang"), anchor_x="center", anchor_y='center')
        if self.index_num >= 1:
            self.save_button.draw()
            self.continue_button.draw()
            aa.draw_text('是否保存', 300, 250, aa.color.WHITE, font_size=15, 
                                font_name=("simhei", "PingFang"), anchor_x="center", anchor_y='center')
            self.open_line.draw()
            aa.draw_text('折线图', 200, 200, aa.color.WHITE, font_size=20, 
                                font_name=("simhei", "PingFang"), anchor_x="center", anchor_y='center')
            self.open_bar.draw()
            aa.draw_text('柱状图', 400, 200, aa.color.WHITE, font_size=20, 
                                font_name=("simhei", "PingFang"), anchor_x="center", anchor_y='center')
            if self.index_num == 1:
                self.open_pie.draw()
                aa.draw_text('饼图', 200, 100, aa.color.WHITE, font_size=20, 
                                    font_name=("simhei", "PingFang"), anchor_x="center", anchor_y='center')
                self.open_radar.draw()
                aa.draw_text('雷达图', 400, 100, aa.color.WHITE, font_size=20, 
                                    font_name=("simhei", "PingFang"), anchor_x="center", anchor_y='center')
        if self.saved1 and time.time() - self.lt1 <= 2:
            aa.draw_text('折线图保存成功', 300, 50, aa.color.WHITE, font_size=20, 
                                font_name=("simhei", "PingFang"), anchor_x="center", anchor_y='center')
        if self.saved2 and time.time() - self.lt2 <= 2:
            aa.draw_text('柱状图保存成功', 300, 50, aa.color.WHITE, font_size=20, 
                                font_name=("simhei", "PingFang"), anchor_x="center", anchor_y='center')
        if self.saved3 and time.time() - self.lt3 <= 2:
            aa.draw_text('雷达图保存成功', 300, 50, aa.color.WHITE, font_size=20, 
                                font_name=("simhei", "PingFang"), anchor_x="center", anchor_y='center')
        if self.saved4 and time.time() - self.lt4 <= 2:
            aa.draw_text('饼图保存成功', 300, 50, aa.color.WHITE, font_size=20, 
                                font_name=("simhei", "PingFang"), anchor_x="center", anchor_y='center')
        if self.saved and time.time() - self.lt <= 2:
            aa.draw_text('全部保存成功', 300, 50, aa.color.WHITE, font_size=20, 
                                font_name=("simhei", "PingFang"), anchor_x="center", anchor_y='center')

    def on_mouse_release(self, x, y, button, modifiers):
        if self.input_file.collides_with_point((x, y)):
            self.root = tk.Tk()
            self.root.withdraw()
            
            csv_path = filedialog.askopenfilename(filetypes=[("CSV文件", "*.csv")])
            df = pd.read_csv(csv_path)
            df.set_index(df.columns[0], inplace=True)
            dft = df.transpose()
            dft.drop(dft.index[0])
            self.index_num = len(dft.columns)

            dft.plot(ax=ax1)
            ax1.set_title('Line Chart')

            dft.plot(kind='bar', ax=ax2)
            ax2.set_title('Bar Chart')

            if self.index_num == 1:
                categories = list(df.columns)
                n = len(categories)
                values = df.values[0].tolist()
                values += values[ : 1]
                angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
                angles += angles[ : 1]
                ax3.plot(angles, values, linewidth=1, linestyle='solid')
                ax3.fill(angles, values, 'b', alpha=0.1)
                ax3.set_xticks(angles[ : -1], categories, color='grey', size=8)
                ax3.set_title('Radar Chart')

                dft.plot(y=dft.columns[0], kind='pie', autopct='%1.1f%%', ax=ax4)
                ax4.set_title('Pie Chart')

            if self.index_num > 1:
                plt.close(fig3)
                plt.close(fig4)
                
            plt.show()

        if self.open_line.collides_with_point((x, y)):
            fig1.savefig('out/line.png')
            self.saved1 = True
            self.lt1 = time.time()

        if self.open_bar.collides_with_point((x, y)):
            fig2.savefig('out/bar.png')
            self.saved2 = True
            self.lt2 = time.time()

        if self.open_radar.collides_with_point((x, y)):
            fig3.savefig('out/radar.png')
            self.saved3 = True
            self.lt3 = time.time()

        if self.open_pie.collides_with_point((x, y)):
            fig4.savefig('out/pie.png')
            self.saved4 = True
            self.lt4 = time.time()

        if self.save_button.collides_with_point((x, y)):
            if self.index_num == 1:
                fig3.savefig('out/radar.png')
                fig4.savefig('out/pie.png')
            fig1.savefig('out/line.png')
            fig2.savefig('out/bar.png')
            self.saved = True
            self.lt = time.time()

        if self.continue_button.collides_with_point((x, y)):
            w.show_view(end)

class End(aa.View):
    def __init__(self):
        super().__init__()
        self.bg = aa.Sprite(background_path, scale=get_scale())
        self.bg.position = 300, 200

    def on_draw(self):
        self.clear()
        self.bg.draw()
        aa.draw_text('感谢使用', 300, 250, aa.color.WHITE, font_size=40, 
                            font_name=("simhei", "PingFang"), anchor_x="center", anchor_y='center')
        aa.draw_text('欢迎您的下次到来', 300, 150, aa.color.WHITE, font_size=30, 
                                font_name=("simhei", "PingFang"), anchor_x="center", anchor_y='center')
    
w = aa.Window(600, 400, '统计图生成器')
start = Start()
process = Process()
end = End()
w.show_view(start)
w.run()