package com.owura.agent

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import java.io.File

class ModelsActivity : AppCompatActivity() {

    private lateinit var modelsList: TextView
    private lateinit var statusText: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_models)

        modelsList = findViewById(R.id.modelsList)
        statusText = findViewById(R.id.statusText)

        loadModels()

        findViewById<Button>(R.id.btnRefresh).setOnClickListener {
            loadModels()
        }

        findViewById<Button>(R.id.btnBack).setOnClickListener {
            finish()
        }
    }

    private fun loadModels() {
        val modelsFile = File("/data/data/com.termux/files/home/.owura-models")

        if (modelsFile.exists()) {
            val content = modelsFile.readText()
            modelsList.text = content
            statusText.text = "Models loaded"
        } else {
            modelsList.text = "No models found.\n\nRun 'owura-update-models' in Termux to fetch available models."
            statusText.text = "No models file"
        }
    }
}
