from django.test import TestCase

# Create your tests here.
from .models import Post


blog_posts = [
    {
        "title": "A Complete Travel Guide to Skardu — The Jewel of Northern Pakistan",
        "content": """
        <h2>Welcome to Skardu – A Paradise for Nature Lovers</h2>
        <p>
        Skardu, the crown jewel of Gilgit-Baltistan, is a place where the mighty mountains meet serene lakes.
        Whether you’re an adventure seeker, a photographer, or simply looking for peace and relaxation,
        Skardu offers an unforgettable experience. The region is home to some of the highest peaks in the world,
        including K2, Broad Peak, and Gasherbrum, making it a dream destination for trekkers and climbers.
        </p>

        <h3>How to Reach Skardu</h3>
        <p>
        You can reach Skardu either by air or road. The <strong>Skardu Airport</strong> connects directly to Islamabad,
        with breathtaking views throughout the flight. Alternatively, the <strong>KKH (Karakoram Highway)</strong> offers
        an adventurous road trip filled with scenic landscapes, rivers, and small mountain towns.
        </p>

        <h3>Top Attractions Near Khar Skardu Hotel</h3>
        <ul>
            <li><strong>Skardu Fort:</strong> A historic monument offering panoramic views of the valley.</li>
            <li><strong>Satpara Lake:</strong> A serene lake perfect for boating and photography.</li>
            <li><strong>Deosai Plains:</strong> Known as the “Roof of the World,” home to Himalayan brown bears and wildflowers.</li>
            <li><strong>Shigar Valley:</strong> Famous for its ancient mosques, fort, and lush orchards.</li>
        </ul>

        <h3>Best Time to Visit</h3>
        <p>
        The best time to visit Skardu is from <strong>April to October</strong>. During these months, the weather is mild,
        roads are open, and the landscapes are at their most vibrant.
        </p>

        <h3>Stay at Khar Skardu Hotel</h3>
        <p>
        If you’re looking for a comfortable stay with scenic views, modern amenities, and warm hospitality,
        <strong>Khar Skardu Hotel</strong> offers the perfect blend of comfort and culture.
        </p>

        <p><em>Plan your next adventure with us and discover the magic of Skardu!</em></p>
        """,
        "tags": "Skardu, Travel, Pakistan, Khar Skardu Hotel, Tourism"
    },
    {
        "title": "Top 7 Things to Do in Skardu for an Unforgettable Vacation",
        "content": """
        <h2>Discover the Magic of Skardu Valley</h2>
        <p>
        Skardu is a destination that offers something for everyone — from tranquil lakes and ancient forts to thrilling
        mountain adventures. Whether you’re staying for a few days or weeks, here are the <strong>top 7 things</strong> 
        you shouldn’t miss during your stay at <strong>Khar Skardu Hotel</strong>.
        </p>

        <h3>1. Visit Shangrila Resort (Lower Kachura Lake)</h3>
        <p>
        Often called “Heaven on Earth,” this picturesque resort is built around a heart-shaped lake surrounded by red-roofed cottages.
        Perfect for a day picnic or romantic evening.
        </p>

        <h3>2. Explore the Historic Skardu Fort</h3>
        <p>
        Located atop a rocky cliff, Skardu Fort offers incredible views of the valley and the Indus River.
        Its centuries-old structure tells tales of Tibetan and Balti rulers who once ruled this region.
        </p>

        <h3>3. Adventure at Deosai National Park</h3>
        <p>
        One of the highest plateaus in the world, Deosai is a UNESCO World Heritage site known for its wildflowers,
        wildlife, and crystal-clear lakes. A must-visit for nature enthusiasts.
        </p>

        <h3>4. Boating at Satpara Lake</h3>
        <p>
        Just 9 km from Skardu, Satpara Lake is a great spot for boating, fishing, and photography.
        The turquoise water with a backdrop of snow-capped peaks looks straight out of a painting.
        </p>

        <h3>5. Experience Balti Culture in Skardu Bazaar</h3>
        <p>
        The vibrant local market is the best place to buy handmade souvenirs, wool shawls, and organic apricot oil.
        Interact with the friendly locals to truly experience Balti hospitality.
        </p>

        <h3>6. Stargazing at Night</h3>
        <p>
        Thanks to its pollution-free skies, Skardu offers some of the clearest night skies in Asia.
        Don’t forget to step outside your hotel and admire the Milky Way!
        </p>

        <h3>7. Stay and Relax at Khar Skardu Hotel</h3>
        <p>
        After a day full of exploration, return to <strong>Khar Skardu Hotel</strong> for a cozy stay.
        Enjoy delicious local cuisine, warm interiors, and stunning views right from your room window.
        </p>
        """,
        "tags": "Things to do in Skardu, Travel, Tourism, Hotels, Khar Skardu Hotel"
    },
    {
        "title": "Why Khar Skardu Hotel is the Best Place to Stay in Skardu",
        "content": """
        <h2>Experience Comfort, Culture, and Charm</h2>
        <p>
        When planning a trip to Skardu, choosing the right accommodation can make or break your experience.
        That’s where <strong>Khar Skardu Hotel</strong> stands out — offering a perfect blend of traditional Balti
        architecture, modern comfort, and exceptional service.
        </p>

        <h3>1. Ideal Location</h3>
        <p>
        Located near the heart of Skardu city, the hotel provides easy access to top attractions like Skardu Fort,
        Satpara Lake, and the bustling local bazaar. You’ll never be far from the action.
        </p>

        <h3>2. Rooms with a View</h3>
        <p>
        Wake up to breathtaking mountain views every morning. Each room is designed to capture the natural beauty
        of the valley while ensuring comfort and privacy for every guest.
        </p>

        <h3>3. Authentic Balti Cuisine</h3>
        <p>
        Enjoy local dishes prepared with organic ingredients sourced from nearby villages. Our in-house restaurant
        serves both traditional and international cuisine, catering to every taste.
        </p>

        <h3>4. Perfect for Every Traveler</h3>
        <p>
        Whether you’re a solo traveler, couple, or family, Khar Skardu Hotel offers the right accommodation for everyone.
        Our staff ensures that each guest enjoys personalized service and memorable experiences.
        </p>

        <h3>5. Easy Booking and Great Offers</h3>
        <p>
        Book directly from our website for exclusive offers and seasonal discounts.
        <strong>No hidden charges, just pure comfort.</strong>
        </p>

        <h3>6. Eco-Friendly Hospitality</h3>
        <p>
        We care deeply for the environment. Our hotel operates with eco-conscious practices including solar heating,
        recycling, and locally sourced materials.
        </p>

        <p><em>When you stay at Khar Skardu Hotel, you’re not just booking a room — you’re becoming part of a story that celebrates the heart of Skardu.</em></p>
        """,
        "tags": "Khar Skardu Hotel, Hotels in Skardu, Accommodation, Travel, Tourism"
    },
]
# http
from django.http import HttpResponse
def create_blog_posts(request):
    for blog in blog_posts:
        Post.objects.create(
            title=blog["title"],
            content=blog["content"],
            tags=blog["tags"],
        )
    return HttpResponse("✅ Blog posts created successfully!")
    
