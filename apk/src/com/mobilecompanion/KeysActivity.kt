package com.mobilecompanion

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import java.io.File

class KeysActivity : AppCompatActivity() {

    private lateinit var googleKey: EditText
    private lateinit var groqKey: EditText
    private lateinit var nvidiaKey: EditText
    private lateinit var ollamaHost: EditText
    private lateinit var statusText: TextView

    private val envFile by lazy { File(filesDir.parentFile, "mobile-companion.env") }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_keys)

        googleKey = findViewById(R.id.googleKey)
        groqKey = findViewById(R.id.groqKey)
        nvidiaKey = findViewById(R.id.nvidiaKey)
        ollamaHost = findViewById(R.id.ollamaHost)
        statusText = findViewById(R.id.statusText)

        loadKeys()

        findViewById<Button>(R.id.btnSave).setOnClickListener {
            saveKeys()
        }

        findViewById<Button>(R.id.btnBack).setOnClickListener {
            finish()
        }
    }

    private fun loadKeys() {
        try {
            if (envFile.exists()) {
                val lines = envFile.readLines()
                for (line in lines) {
                    when {
                        line.startsWith("GOOGLE_AI_STUDIO_KEY=") -> googleKey.setText(line.substringAfter("="))
                        line.startsWith("GROQ_API_KEY=") -> groqKey.setText(line.substringAfter("="))
                        line.startsWith("NVIDIA_API_KEY=") -> nvidiaKey.setText(line.substringAfter("="))
                        line.startsWith("OLLAMA_HOST=") -> ollamaHost.setText(line.substringAfter("="))
                    }
                }
                statusText.text = "Keys loaded"
            }
        } catch (e: Exception) {
            statusText.text = "Error loading keys"
        }
    }

    private fun saveKeys() {
        try {
            val content = """
                |GOOGLE_AI_STUDIO_KEY=${googleKey.text}
                |GROQ_API_KEY=${groqKey.text}
                |NVIDIA_API_KEY=${nvidiaKey.text}
                |OLLAMA_HOST=${ollamaHost.text}
            """.trimMargin()
            envFile.writeText(content)
            statusText.text = "Keys saved!"
            Toast.makeText(this, "API keys saved", Toast.LENGTH_SHORT).show()
        } catch (e: Exception) {
            statusText.text = "Error saving keys"
        }
    }
}
