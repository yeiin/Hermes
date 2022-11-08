package com.example.hermes_application;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;

public class BabyVideoActivity extends AppCompatActivity {

    private WebView mWebView;
    private WebSettings mWebSettings;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_baby_video);

        Button button_previous = (Button) findViewById(R.id.button_second);
        mWebView = (WebView)findViewById(R.id.video);

        mWebView.clearCache(true);
        mWebView.clearHistory();
        mWebView.setWebViewClient(new WebViewClient()); //click시 새창 안뜨게
        mWebSettings = mWebView.getSettings(); //세부 세팅 등록
        mWebSettings.setJavaScriptEnabled(true); //웹페이지 자바스크립트 허용 여부
        mWebSettings.setSupportMultipleWindows(false); //새창 띄우기 허용 여부
        mWebSettings.setJavaScriptCanOpenWindowsAutomatically(false); //자바스크립트 새창 띄우기(멀티뷰) 허용 여부
        mWebSettings.setLoadWithOverviewMode(true); //메타태그 허용 여부
        mWebSettings.setUseWideViewPort(true); //화면 사이즈 맞추기 허용 여부
        mWebSettings.setSupportZoom(false); //화면 줌 허용 여부
        mWebSettings.setBuiltInZoomControls(false); //화면 확대 축소 허용 여부
        mWebSettings.setLayoutAlgorithm(WebSettings.LayoutAlgorithm.SINGLE_COLUMN); //컨텐츠 사이즈 맞추기
        mWebSettings.setCacheMode(WebSettings.LOAD_NO_CACHE); //브라우저 캐시 허용 여부
        mWebSettings.setDomStorageEnabled(true); //로컬저장소 허용 여부

        mWebView.loadUrl("http://192.168.0.17:5000/"); // 웹뷰에 표시할 라즈베리파이 주소, 웹뷰 시작
//        mWebView.loadUrl("https://www.youtube.com/watch?v=CMtVHJX6Pxc");

        button_previous.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });
    }
}