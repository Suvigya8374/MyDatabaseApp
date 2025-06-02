import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import mysql.connector
import asyncio
import platform
import os
kivy.require('2.0.0')

class DatabaseApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Database connection configuration (using environment variables for security)
        self.db_config = {
            'host': os.getenv('DB_HOST', '103.239.139.219'),
            'database': os.getenv('DB_NAME', 'vtechtest'),
            'user': os.getenv('DB_USER', 'vtech'),
            'password': os.getenv('DB_PASS', 'Vtech@12@'),
            'port': int(os.getenv('DB_PORT', 3306))
        }
        
        # UI Elements
        self.title_label = Label(
            text='SQL Table Data Viewer',
            size_hint=(1, 0.1),
            font_size='20sp'
        )
        
        self.fetch_button = Button(
            text='Fetch Data from Database',
            size_hint=(1, 0.1),
            on_press=self.fetch_data
        )
        
        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.table_layout = GridLayout(cols=1, size_hint_y=None)
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))
        self.scroll_view.add_widget(self.table_layout)
        
        # Add widgets to layout
        self.add_widget(self.title_label)
        self.add_widget(self.fetch_button)
        self.add_widget(self.scroll_view)

    def fetch_data(self, instance):
        try:
            # Connect to the database
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            # Fetch the list of tables
            cursor.execute("SHOW TABLES")
            tables = [row[0] for row in cursor.fetchall()]
            
            # Clear previous table data
            self.table_layout.clear_widgets()
            
            # Display the list of tables
            tables_label = Label(
                text="Tables in vtechtest database: " + ", ".join(tables),
                size_hint_y=None,
                height=40,
                bold=True,
                font_size='18sp'
            )
            self.table_layout.add_widget(tables_label)
            
            # Fetch data from a specific table (default to the first table)
            if tables:
                table_name = tables[0]  # Use the first table; can be modified to select dynamically
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                # Add table name as a header
                table_label = Label(
                    text=f'Table: {table_name}',
                    size_hint_y=None,
                    height=40,
                    bold=True,
                    font_size='18sp'
                )
                self.table_layout.add_widget(table_label)
                
                # Create header row for the table
                header = GridLayout(cols=len(columns), size_hint_y=None, height=40)
                for col in columns:
                    header.add_widget(Label(text=str(col), bold=True, size_hint_y=None, height=40))
                self.table_layout.add_widget(header)
                
                # Add data rows
                for row in rows:
                    row_layout = GridLayout(cols=len(columns), size_hint_y=None, height=40)
                    for value in row:
                        row_layout.add_widget(Label(text=str(value), size_hint_y=None, height=40))
                    self.table_layout.add_widget(row_layout)
            else:
                self.table_layout.add_widget(Label(
                    text="No tables found in the database.",
                    size_hint_y=None,
                    height=40
                ))
            
            # Close connection
            cursor.close()
            connection.close()
            
        except mysql.connector.Error as err:
            self.table_layout.clear_widgets()
            self.table_layout.add_widget(Label(
                text=f"Error: {str(err)}",
                size_hint_y=None,
                height=40
            ))

class MySQLApp(App):
    def build(self):
        return DatabaseApp()

async def main():
    app = MySQLApp()
    app.build()
    await asyncio.sleep(1.0 / 60)  # Control frame rate

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(MySQLApp().run())