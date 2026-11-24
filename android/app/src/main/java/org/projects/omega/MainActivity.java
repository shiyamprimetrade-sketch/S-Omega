package org.projects.omega;
import android.app.Activity;
import android.os.Bundle;
import android.widget.*;
import android.graphics.Color;
import java.security.MessageDigest;
import java.nio.charset.StandardCharsets;

public class MainActivity extends Activity {
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        LinearLayout layout=new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(32,64,32,32);
        layout.setBackgroundColor(Color.rgb(18,22,30));
        TextView title=new TextView(this);
        title.setText("S-Omega | Developer Preview");
        title.setTextSize(24);
        title.setTextColor(Color.WHITE);
        layout.addView(title);
        EditText input=new EditText(this);
        input.setHint("Enter text to fingerprint");
        layout.addView(input);
        TextView output=new TextView(this);
        output.setTextColor(Color.WHITE);
        Button button=new Button(this);
        button.setText("Generate SHA-256 fingerprint");
        layout.addView(button);
        layout.addView(output);
        button.setOnClickListener(v -> {
            try {
                byte[] hash=MessageDigest.getInstance("SHA-256").digest(input.getText().toString().getBytes(StandardCharsets.UTF_8));
                StringBuilder hex=new StringBuilder();
                for(byte x:hash) hex.append(String.format(java.util.Locale.ROOT,"%02x",x & 255));
                output.setText(hex.toString());
            } catch(Exception e) { output.setText("Fingerprint failed"); }
        });
        setContentView(layout);
    }
}
