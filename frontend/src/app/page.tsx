/**
 * Why: The home route should compose sections without owning their internals.
 * What: Renders the polished recruiter-facing landing page shell.
 * How: Imports server/client section components from feature-neutral folders.
 */
import { ArchitectureSection } from "@/components/sections/architecture-section";
import { HeroSection } from "@/components/sections/hero-section";
import { RecruiterSection } from "@/components/sections/recruiter-section";
import { SupportedPlatformsSection } from "@/components/sections/supported-platforms-section";
import { Footer } from "@/components/site/footer";
import { Navbar } from "@/components/site/navbar";

export default function Home() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen overflow-hidden bg-background">
        <HeroSection />
        <SupportedPlatformsSection />
        <ArchitectureSection />
        <RecruiterSection />
      </main>
      <Footer />
    </>
  );
}
