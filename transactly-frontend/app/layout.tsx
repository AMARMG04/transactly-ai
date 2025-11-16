import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: 'Transactly — Demo',
  description: 'Privacy-first explainable transaction classifier demo'
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      {/* <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body> */}
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen flex flex-col items-center px-4`}>
        <header className="w-full max-w-4xl py-8">
          <h1 className="text-4xl font-semibold tracking-tight">Transactly</h1>
          <p className="text-sm text-muted mt-1">
            Privacy-first explainable transaction classifier
          </p>
        </header>

        <main className="w-full max-w-4xl space-y-8 pb-20">
          {children}
        </main>
      </body>
    </html>
  );
}
