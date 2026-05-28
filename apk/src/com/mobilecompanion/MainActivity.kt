package com.owura.agent

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import java.io.File

class MainActivity : AppCompatActivity() {

    private lateinit var statusText: TextView
    private lateinit var termuxStatus: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        statusText = findViewById(R.id.statusText)
        termuxStatus = findViewById(R.id.termuxStatus)

        checkTermuxStatus()

        findViewById<Button>(R.id.btnSetup).setOnClickListener {
            startActivity(Intent(this, SetupActivity::class.java))
        }

        findViewById<Button>(R.id.btnKeys).setOnClickListener {
            startActivity(Intent(this, KeysActivity::class.java))
        }

        findViewById<Button>(R.id.btnModels).setOnClickListener {
            startActivity(Intent(this, ModelsActivity::class.java))
        }

        findViewById<Button>(R.id.btnOpenTermux).setOnClickListener {
            openTermux()
        }
    }

    private fun checkTermuxStatus() {
        val termuxDir = File("/data/data/com.termux")
        val owuraDir = File("/data/data/com.termux/files/home/owura")

        if (termuxDir.exists()) {
            termuxStatus.text = "Termux: Installed"
            termuxStatus.setTextColor(getColor(R.color.green))
        } else {
            termuxStatus.text = "Termux: Not Found"
            termuxStatus.setTextColor(getColor(R.color.red))
        }

        if (owuraDir.exists()) {
            statusText.text = "OWURA: Ready"
            statusText.setTextColor(getColor(R.color.green))
        } else {
            statusText.text = "OWURA: Not Setup"
            statusText.setTextColor(getColor(R.color.orange))
        }
    }

    private fun openTermux() {
        val intent = packageManager.getLaunchIntentForPackage("com.termux")
        if (intent != null) {
            startActivity(intent)
        } else {
            statusText.text = "Termux not installed!"
            statusText.setTextColor(getColor(R.color.red))
        }
    }
}
