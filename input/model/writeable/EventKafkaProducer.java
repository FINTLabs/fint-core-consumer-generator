package no.fintlabs.consumer.model.MODEL_LOWER;

import no.fintlabs.core.consumer.shared.resource.kafka.EventKafkaProducer;
import no.fintlabs.kafka.event.EventProducerFactory;
import no.fintlabs.kafka.event.topic.EventTopicService;
import org.springframework.stereotype.Service;

@Service
public class MODELEventKafkaProducer extends EventKafkaProducer {
    public MODELEventKafkaProducer(EventProducerFactory eventProducerFactory, MODELConfig MODEL_LOWERConfig, EventTopicService eventTopicService) {
        super(eventProducerFactory, MODEL_LOWERConfig, eventTopicService);
    }
}
