package com.mobilecompanion

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Button
import android.widget.CheckBox
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class SetupActivity : AppCompatActivity() {

    private lateinit var step1Check: CheckBox
    private lateinit var step2Check: CheckBox
    private lateinit var step3Check: CheckBox
    private lateinit var step4Check: CheckBox
    private lateinit var statusText: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_setup)

        step1Check = findViewById(R.id.step1Check)
        step2Check = findViewById(R.id.step2Check)
        step3Check = findViewById(R.id.step3Check)
        step4Check = findViewById(R.id.step4Check)
        statusText = findViewById(R.id.statusText)

        findViewById<Button>(R.id.btnInstallTermux).setOnClickListener {
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://f-droid.org/en/packages/com.termux/"))
            startActivity(intent)
        }

        findViewById<Button>(R.id.btnInstallApi).setOnClickListener {
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://f-droid.org/en/packages/com.termux.api/"))
            startActivity(intent)
        }

        findViewById<Button>(R.id.btnCopyClone).setOnClickListener {
            val clipboard = getSystemService(CLIPBOARD_SERVICE) as android.content.ClipboardManager
            val clip = android.content.ClipData.newPlainText("command", "git clone https://github.com/agyeiboaduandy-crypto/mobile-companion.git")
            clipboard.setPrimaryClip(clip)
            statusText.text = "Command copied!"
        }

        findViewById<Button>(R.id.btnCopySetup).setOnClickListener {
            val clipboard = getSystemService(CLIPBOARD_SERVICE) as android.content.ClipboardManager
            val clip = android.content.ClipData.newPlainText("command", "cd mobile-companion && bash scripts/bootstrap.sh")
            clipboard.setPrimaryClip(clip)
            statusText.text = "Command copied!"
        }

        findViewById<Button>(R.id.btnBack).setOnClickListener {
            finish()
        }
    }
}
